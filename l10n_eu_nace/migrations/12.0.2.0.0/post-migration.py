# Copyright 2019 ACSONE SA/NV
# Copyright 2020 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env):
    nace_categories = env['ir.model_data'].search(
        [
            ('module', '=', 'l10_eu_nace'),
            ('model', '=', 'res.partner.category'),
        ]
    )
    for category_imd in nace_categories:
        partners = env['res.partner'].search(
            [('category_id', 'in', [category_imd.res_id])]
        )

        partners.write(
            {
                'nace_id': env.ref(
                    'l10n_eu_nace.%s'
                    % category_imd.name.replace('old_', '', 1)
                ).id
            }
        )
