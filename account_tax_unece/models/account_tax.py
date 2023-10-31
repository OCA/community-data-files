# Copyright 2016-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    unece_type_id = fields.Many2one(
        "unece.code.list",
        string="UNECE Tax Type",
        domain=[("type", "=", "tax_type")],
        ondelete="restrict",
        help="Select the Tax Type Code of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement 5153",
    )
    unece_type_code = fields.Char(
        related="unece_type_id.code",
        store=True,
        readonly=True,
        string="UNECE Type Code",
    )
    unece_categ_id = fields.Many2one(
        "unece.code.list",
        string="UNECE Tax Category",
        domain=[("type", "=", "tax_categ")],
        ondelete="restrict",
        help="Select the Tax Category Code of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement 5305",
    )
    unece_categ_code = fields.Char(
        related="unece_categ_id.code",
        store=True,
        readonly=True,
        string="UNECE Category Code",
    )
    # We now have a selection field "tax_exigibility"
    # with 2 possible values: "on_invoice" or "on_payment"
    # So we don't need the field unece_due_date_id any more.
    # We replace it by _get_unece_due_date_type_code() below.

    @api.model
    def _get_unece_code_from_tax_exigibility(self, tax_exigibility):
        mapping = {
            "on_invoice": "5",
            "on_payment": "72",
        }
        return mapping.get(tax_exigibility)

    @api.model
    def _get_tax_exigibility_from_unece_code(self, unece_code):
        if isinstance(unece_code, int):
            unece_code = str(unece_code)
        mapping = {
            "5": "on_invoice",
            "29": "on_invoice",
            "72": "on_payment",
        }
        if unece_code in mapping:
            return mapping[unece_code]
        else:
            return None

    def _get_unece_due_date_type_code(self):
        self.ensure_one()
        if self.tax_exigibility:
            return self._get_unece_code_from_tax_exigibility(self.tax_exigibility)
        else:
            return None
