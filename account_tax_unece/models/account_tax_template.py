# Copyright 2017-2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTaxTemplate(models.Model):
    _inherit = "account.tax.template"

    unece_type_id = fields.Many2one(
        "unece.code.list",
        string="UNECE Tax Type",
        domain=[("type", "=", "tax_type")],
        help="Select the Tax Type Code of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement 5153",
    )
    unece_categ_id = fields.Many2one(
        "unece.code.list",
        string="UNECE Tax Category",
        domain=[("type", "=", "tax_categ")],
        help="Select the Tax Category Code of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement 5305",
    )

    def _get_tax_vals(self, company, tax_template_to_tax):
        self.ensure_one()
        res = super()._get_tax_vals(company, tax_template_to_tax)
        res["unece_type_id"] = self.unece_type_id.id
        res["unece_categ_id"] = self.unece_categ_id.id
        return res
