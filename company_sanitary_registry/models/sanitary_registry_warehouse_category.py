# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import api, fields, models


class SanitaryRegistryWarehouseCategory(models.Model):
    _name = "sanitary.registry.warehouse.category"
    _description = "Sanitary Registry Warehouse Category"

    sanitary_registry_id = fields.Many2one("sanitary.registry", required=True)
    category_id = fields.Many2one("product.category")
    category_complete_name = fields.Char(related="category_id.complete_name")
    warehouse_id = fields.Many2one("stock.warehouse")

    @api.model
    def get_active_sanitary_registry(self, category, warehouse):
        """Method to get the most specific sanitary registry for a given
        product category and warehouse.
        """
        category_ids = [category.id]
        while category.parent_id:
            category = category.parent_id
            category_ids.append(category.id)
        sanitary_registries = self.search(
            [
                "|",
                ("category_id", "in", category_ids),
                ("category_id", "=", False),
                "|",
                ("warehouse_id", "=", warehouse.id),
                ("warehouse_id", "=", False),
            ]
        )
        sanitary_registry = sanitary_registries.sorted(
            lambda sr: (sr.category_complete_name or "", 1 if sr.warehouse_id else 0),
            reverse=True,
        )[:1]
        return sanitary_registry.sanitary_registry_id
