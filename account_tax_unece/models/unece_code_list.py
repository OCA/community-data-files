# Copyright 2016-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class UneceCodeList(models.Model):
    _inherit = "unece.code.list"

    type = fields.Selection(
        selection_add=[
            ("tax_type", "Tax Types (UNCL 5153)"),
            ("tax_categ", "Tax Categories (UNCL 5305)"),
        ],
        ondelete={
            "tax_type": "cascade",
            "tax_categ": "cascade",
        },
    )
