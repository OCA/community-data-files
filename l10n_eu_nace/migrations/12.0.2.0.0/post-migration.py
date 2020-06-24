# Copyright 2019 ACSONE SA/NV
# Copyright 2020 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    cr.execute(
        """
            UPDATE res_partner rp
            SET nace_id = imd2.res_id
            FROM ir_model_data imd1
            LEFT JOIN ir_model_data imd2
                ON  imd2.module = imd1.module
                AND imd2.name = substring(imd1.name, 5)
            WHERE imd1.name LIKE 'old_%'
                AND rp.category_id = imd1.res_is
            """
    )
