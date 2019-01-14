# Copyright 2016 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductUom(models.Model):
    _inherit = 'product.uom'

    unece_code = fields.Char(
        string='UNECE Code',
        help="Standard nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE).")
