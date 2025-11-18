# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    sanitary_registry_id = fields.Many2one("sanitary.registry")

    def get_sanitary_registry(self):
        self.ensure_one()
        if self.sanitary_registry_id:
            return self.sanitary_registry_id
        elif self.parent_id:
            return self.parent_id.get_sanitary_registry()
        return self.sanitary_registry_id
