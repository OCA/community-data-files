# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    sds = fields.Char(string="SDS")
    content_package = fields.Float(string="Content Packaging")
