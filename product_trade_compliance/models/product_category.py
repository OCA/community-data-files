# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    compliance_code_id = fields.Many2one(
        comodel_name="trade.compliance.code",
        string="Default Compliance Code",
        help="Default Dual-Use or export control code for products in this category",
    )
