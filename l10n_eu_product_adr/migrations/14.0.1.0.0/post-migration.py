# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

"""Sets the adr goods id on the products according to their
adr_number / transport_category (set in the pre migration script).

This is required because the information has been lost in the
l10n_eu_product_adr migration process
"""


def assign_adr_class(cr):
    query = """
        UPDATE product_product
        SET adr_goods_id = subquery.adr_goods_id
        FROM (
            SELECT ag.id as adr_goods_id, array_agg(pp.id) as product_ids
            FROM product_product pp
            INNER JOIN adr_goods ag ON (
                pp.adr_number = ag.un_number
                AND pp.transport_category = ag.transport_category
            )
            WHERE pp.adr_number IS NOT NULL
            GROUP BY ag.id
        ) AS subquery
        WHERE product_product.id = ANY(subquery.product_ids);
    """
    cr.execute(query)


def cleanup_adr_code(cr):
    cr.execute("ALTER TABLE product_product DROP adr_number;")


def migrate(cr, version):
    assign_adr_class(cr)
    cleanup_adr_code(cr)
