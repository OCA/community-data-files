# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    all_taxes = (
        env["account.tax"]
        .with_context(active_test=False)
        .search([("type_tax_use", "=", "sale")])
    )
    # _compute_unece_vatex_id() uses the VATEX codes identified by XMLID
    # So we must re-run the compute method after the creation of the VATEX codes
    all_taxes._compute_unece_vatex_id()
