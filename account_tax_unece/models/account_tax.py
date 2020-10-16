# Copyright 2016-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
    # So we don't need unece_due_date_id any more
