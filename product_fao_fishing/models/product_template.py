# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fao_fishing_area_ids = fields.Many2many(
        comodel_name="product.attribute.value", compute="_compute_fao_fishing_area_ids"
    )
    fao_fishing_technique_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        compute="_compute_fao_fishing_technique_ids",
    )

    def _compute_fao_fishing_area_ids(self):
        """
        Helper method to retrieve the fishing areas from product attributes
        """
        fao_fishing_area_attribute = self.env.ref(
            "product_fao_fishing.fao_fishing_area"
        )
        ptal_obj = self.env["product.template.attribute.line"]
        for template in self:
            attribute_line = ptal_obj.search(
                [
                    ("product_tmpl_id", "=", template.id),
                    ("attribute_id", "=", fao_fishing_area_attribute.id),
                ]
            )
            template.fao_fishing_area_ids = attribute_line.value_ids

    def _compute_fao_fishing_technique_ids(self):
        """
        Helper method to retrieve the fishing areas from product attributes
        """
        fao_fishing_technique_attribute = self.env.ref(
            "product_fao_fishing.fao_fishing_technique"
        )
        ptal_obj = self.env["product.template.attribute.line"]
        for template in self:
            attribute_line = ptal_obj.search(
                [
                    ("product_tmpl_id", "=", template.id),
                    ("attribute_id", "=", fao_fishing_technique_attribute.id),
                ]
            )
            template.fao_fishing_technique_ids = attribute_line.value_ids
