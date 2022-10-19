# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    unece_code = fields.Char(
        string="UNECE Code",
        help="Standard nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE).",
    )
