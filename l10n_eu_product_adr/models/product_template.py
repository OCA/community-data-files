# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# Copyright 2021 Opener B.V. <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    adr_goods_on_variants = fields.Boolean(
        compute="_compute_adr_goods_on_variants",
        help="Indicates whether the adr configuration is different for each variant.",
    )
    is_dangerous = fields.Boolean(
        related="product_variant_ids.is_dangerous",
        readonly=False,
        help="This product belongs to a dangerous class",
    )
    adr_goods_id = fields.Many2one(
        "adr.goods",
        "Dangerous Goods",
        related="product_variant_ids.adr_goods_id",
        readonly=False,
    )
    adr_class_id = fields.Many2one(
        "adr.class", related="product_variant_ids.adr_goods_id.class_id"
    )
    adr_classification_code = fields.Char(related="adr_goods_id.classification_code")
    adr_label_ids = fields.Many2many(
        "adr.label", related="product_variant_ids.adr_goods_id.label_ids"
    )
    adr_limited_quantity = fields.Float(
        related="product_variant_ids.adr_goods_id.limited_quantity",
    )
    adr_limited_quantity_uom_id = fields.Many2one(
        related="product_variant_ids.adr_goods_id.limited_quantity_uom_id",
    )
    adr_packing_instruction_ids = fields.Many2many(
        "adr.packing.instruction",
        related="product_variant_ids.adr_goods_id.packing_instruction_ids",
    )
    adr_transport_category = fields.Selection(
        related="product_variant_ids.adr_goods_id.transport_category"
    )
    adr_tunnel_restriction_code = fields.Selection(
        related="product_variant_ids.adr_goods_id.tunnel_restriction_code",
    )

    @api.depends("product_variant_ids.adr_goods_id")
    def _compute_adr_goods_on_variants(self):
        for template in self:
            template.adr_goods_on_variants = not all(
                product.adr_goods_id == (template.product_variant_ids[0].adr_goods_id)
                for product in template.product_variant_ids[1:]
            )

    def write(self, values):
        """Delegate dangerous goods fields to variants

        while preventing a sweeping change over variants with different settings
        """
        values = values.copy()
        variant_vals = {}
        for field in ("is_dangerous", "adr_goods_id"):
            if field in values:
                variant_vals[field] = values.pop(field)
        res = super().write(values)
        if variant_vals:
            if any(template.adr_goods_on_variants for template in self):
                raise UserError(
                    self.env._(
                        "There are different dangerous goods configured on "
                        "this product's variant, so you cannot update the "
                        "dangerous goods from here. Please reconfigure each "
                        "variant separately."
                    )
                )
            self.mapped("product_variant_ids").write(variant_vals)
        return res

    @api.onchange("is_dangerous")
    def onchange_is_dangerous(self):
        """Remove the dangerous goods attribute from the product

        (when is_dangerous is deselected)
        """
        if not self.is_dangerous and self.adr_goods_id:
            self.adr_goods_id = False

    @api.model_create_multi
    def create(self, vals_list):
        """Propagate the template's adr settings on the created variants"""
        res = super().create(vals_list)
        for template, vals in zip(res, vals_list, strict=False):
            variant_vals = {}
            for field in ("is_dangerous", "adr_goods_id"):
                if field in vals:
                    variant_vals[field] = vals[field]
                if variant_vals:
                    template.product_variant_ids.write(variant_vals)
        return res
