# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPackagingLevel(models.Model):

    _inherit = "product.packaging.level"

    unece_type_ids = fields.Many2many(
        comodel_name="unece.code.list",
        string="UNECE Packaging Types",
        domain=[("type", "=", "packaging_type")],
        help="Select the Packaging Type Codes of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement Rec 21)",
    )
