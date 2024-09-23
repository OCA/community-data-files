# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)


from psycopg2.extras import Json

from odoo import SUPERUSER_ID, api, tools


def migrate(cr, version):
    """Merge res.partner.nace with res.partner.industry
    ============================================================================
    The field mapping is the following:
    res.partner.nace -> res.partner.industry
    - name           -> name
    - name + code    -> full_name
    - parent_id      -> parent_id
    - child_ids      -> child_ids
    - active         -> active
    """
    # 1. Convert column name to jsonb if it is varchar
    table_columns_nace = tools.sql.table_columns(cr, "res_partner_nace")
    if table_columns_nace["name"]["udt_name"] == "varchar":
        tools.sql.convert_column_translatable(cr, "res_partner_nace", "name", "jsonb")
    # 2. Load translation for name from _ir_translation
    cr.execute(
        """
        WITH t AS (
            SELECT
                it.res_id as res_id,
                jsonb_object_agg(it.lang, it.value) AS value
            FROM _ir_translation it
            where it.type = 'model' and it.name = 'res.partner.nace,name' GROUP BY it.res_id
        )
        UPDATE res_partner_nace rpn
        SET name = t.value || rpn.name
        FROM t
        WHERE rpn.id = t.res_id
        """
    )
    # 3. Insert res_partner_industry from res_partner_nace
    cr.execute(
        """
        SELECT
            id,
            code,
            name,
            parent_id
        FROM res_partner_nace
        """
    )
    naces = cr.dictfetchall()
    for nace in naces:
        nace["full_name"] = {
            lang: f"{nace['code']} - {name}" if nace["code"] else name
            for lang, name in nace["name"].items()
        }
    cr.execute(
        """
        WITH naces AS (
            SELECT
                id,
                full_name
            FROM jsonb_to_recordset(%s) AS x (
                id INT,
                full_name JSONB
            )
        )
        INSERT INTO res_partner_industry (
            name,
            full_name,
            active,
            create_uid,
            create_date,
            write_uid,
            write_date
        )
        SELECT
            rpn.name,
            naces.full_name,
            rpn.active,
            rpn.create_uid,
            rpn.create_date,
            rpn.write_uid,
            rpn.write_date
        FROM res_partner_nace rpn
        INNER JOIN naces ON rpn.id = naces.id
        RETURNING full_name->>'en_US', id
        """,
        (Json(naces),),
    )
    new_industries = dict(cr.fetchall())
    for nace in naces:
        nace["industry_id"] = new_industries[nace["full_name"]["en_US"]]
    # 4. Update the parent_id from res_partner_industry
    cr.execute(
        """
        WITH naces AS (
            SELECT
                id,
                parent_id,
                industry_id
            FROM jsonb_to_recordset(%s) AS x (
                id INT,
                parent_id INT,
                industry_id INT
            )
        )
        UPDATE res_partner_industry
        SET parent_id = n2.industry_id
        FROM naces n1
        INNER JOIN naces n2 ON n1.parent_id = n2.id
        WHERE res_partner_industry.id = n1.industry_id
        """,
        (Json(naces),),
    )
    # 5. Run the parent_path computation
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["res.partner.industry"]._parent_store_compute()
    # 6. Update res_partner with the new industry_id
    cr.execute(
        """
        WITH naces AS (
            SELECT
                id,
                industry_id
            FROM jsonb_to_recordset(%s) AS x (
                id INT,
                industry_id INT
            )
        )
        UPDATE res_partner
        SET industry_id = naces.industry_id
        FROM naces
        WHERE nace_id IS NOT NULL and nace_id = naces.id
        """,
        (Json(naces),),
    )
    # 7. Update res_partner with the new secondary_industry_ids
    cr.execute(
        """
        WITH naces AS (
            SELECT
                id,
                industry_id
            FROM jsonb_to_recordset(%s) AS x (
                id INT,
                industry_id INT
            )
        )
        INSERT INTO res_partner_res_partner_industry_rel (
            res_partner_id,
            res_partner_industry_id
        )
        SELECT
            rprpnr.res_partner_id,
            naces.industry_id
        FROM res_partner_res_partner_nace_rel rprpnr
        INNER JOIN naces ON rprpnr.res_partner_nace_id = naces.id
        WHERE rprpnr.res_partner_nace_id = naces.id
        """,
        (Json(naces),),
    )
