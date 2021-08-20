# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductDangerousClass(models.Model):
    _name = "product.dangerous.class"
    _description = "Product Dangerous Class"
    _rec_name = "complete_name"

    name = fields.Char(required=True, translate=True)
    complete_name = fields.Char(compute="_compute_complete_name")
    code = fields.Char(required=True)
    image = fields.Binary(string="Icon", required=True)
    class_type_id = fields.Many2one(
        comodel_name="product.dangerous.class.type",
        ondelete="restrict",
        string="Dangerous Type",
    )

    @api.depends("name", "code")
    def _compute_complete_name(self):
        for record in self:
            record.complete_name = " ".join([record.code, record.name])

    _sql_constraints = [("code_unique", "unique(code)", "This code already exist")]


class ProductDangerousClassType(models.Model):
    _name = "product.dangerous.class.type"
    _description = "Product Dangerous Type"

    name = fields.Char(required=True, translate=True)
    division = fields.Char()
