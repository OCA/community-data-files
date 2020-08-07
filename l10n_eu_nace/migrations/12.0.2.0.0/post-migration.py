# Copyright 2019 ACSONE SA/NV
# Copyright 2020 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    cr.execute(
        """
        WITH imd_new AS(
            SELECT 
                imd_new.name AS xml_id, 
                imd_new.res_id AS new_res_id
            FROM ir_model_data AS imd_new
            WHERE imd_new.name NOT LIKE 'old_%' 
            AND imd_new.module = 'l10n_eu_nace'
        ),
        imd_old AS(
            SELECT 
                substring(imd_old.name, 5) AS xml_id, 
                imd_old.res_id AS old_res_id
            FROM ir_model_data AS imd_old
            WHERE imd_old.name LIKE 'old_%' 
            AND imd_old.module = 'l10n_eu_nace'
        ),
        match_old_new AS(
            SELECT 
                imd_new.xml_id,
                imd_new.new_res_id,
                imd_old.old_res_id
            FROM imd_new
            INNER JOIN imd_old ON imd_new.xml_id = imd_old.xml_id
        ),
        partner_with_old_nace AS(
            SELECT 
                rp.id AS part_id,
                rp.name,
                rpc.category_id,
                match_old_new.new_res_id
            FROM res_partner AS rp
            INNER JOIN res_partner_res_partner_category_rel AS rpc ON rpc.partner_id = rp.id
            INNER JOIN match_old_new ON match_old_new.old_res_id = rpc.category_id
            
        )
        UPDATE res_partner rp
        SET nace_id = partner_with_old_nace.new_res_id
        FROM partner_with_old_nace
        WHERE rp.id = partner_with_old_nace.part_id;
            """
    )
