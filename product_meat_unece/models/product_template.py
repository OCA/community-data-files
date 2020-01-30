# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    unece_meat_code = fields.Char(
        string="UNECE Meat Code",
        compute="_compute_unece_meat_code",
        readonly=True,
        store=True,
    )
    unece_meat_species_id = fields.Many2one(
        string="Species",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_species")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_product_cut_id = fields.Many2one(
        string="Product/cut",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_product_cut")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_refrigeration_id = fields.Many2one(
        string="Refrigeration",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_refrigeration")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_bovine_category_id = fields.Many2one(
        string="Bovine category",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_bovine_category")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_production_system_id = fields.Many2one(
        string="Production system",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_production_system")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_feeding_system_id = fields.Many2one(
        string="Feeding system",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_feeding_system")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_slaughter_system_id = fields.Many2one(
        string="Slaughter system",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_slaughter_system")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_post_slaughter_system_id = fields.Many2one(
        string="Post-slaughter system",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_post_slaughter_system")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_fat_thickness_id = fields.Many2one(
        string="Fat thickness",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_fat_thickness")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_bovine_quality_system_id = fields.Many2one(
        string="Bovine quality system",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_bovine_quality_system")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_weight_range_id = fields.Many2one(
        string="Weight range",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_weight_range")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_packing_id = fields.Many2one(
        string="Packing",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_packing")],
        ondelete="restrict",
        unece_meat_code=True,
    )
    unece_meat_conformity_assessment_id = fields.Many2one(
        string="Conformity assessment",
        comodel_name="unece.code.list",
        domain=[("type", "=", "meat_conformity_assessment")],
        ondelete="restrict",
        unece_meat_code=True,
    )

    @api.model
    def _get_unece_meat_fields(self):
        res = []
        for f in self._fields.values():
            if f._attrs.get("unece_meat_code"):
                res.append(f)
        return res

    @api.model
    def _prepare_get_product_from_unece_domain(self, product=False, **kwargs):
        product_model = self.env["product.template"]
        if not product:
            product = product_model.browse()
            domain = []
        else:
            domain = [("id", "!=", product.id)]
        for product_field in self._get_unece_meat_fields():
            field_name = product_field.name
            val = kwargs.get(field_name, False) or product[field_name].code
            domain.append((field_name + ".code", "=", val))
        return domain

    @api.model
    def _get_product_from_unece(self, product=False, **kwargs):
        """
        This method fetches the product template(s) matching the the given codes or
        the given product template codes (if given).
        Example: _get_product_from_unece(product_01, unece_meat_packing_id='1') will
        search for a product template matching all the UNECE codes of product_01
        but with unece_meat_packing_id.code == '1'.
        :param product: product.template instance
        :param kwargs: UNECE code values
        :return: product.template instance != product
        """
        product_model = self.env["product.template"]
        domain = self._prepare_get_product_from_unece_domain(product=product, **kwargs)
        return product_model.search(domain)

    @api.depends(lambda self: [f.name for f in self._get_unece_meat_fields()])
    def _compute_unece_meat_code(self):
        for rec in self:
            rec.unece_meat_code = (
                "{species}{product_cut}00{refrigeration}{bovine_category}"
                "{production_system}{feeding_system}{slaughter_system}"
                "{post_slaughter_system}{fat_thickness}{quality_system}{weight_range}"
                "{packing}{conformity_assessment}".format(
                    species=rec.unece_meat_species_id.code or "00",
                    product_cut=rec.unece_meat_product_cut_id.code or "0000",
                    refrigeration=rec.unece_meat_refrigeration_id.code or "00",
                    bovine_category=rec.unece_meat_bovine_category_id.code or "0",
                    production_system=rec.unece_meat_production_system_id.code or "0",
                    feeding_system=rec.unece_meat_feeding_system_id.code or "0",
                    slaughter_system=rec.unece_meat_slaughter_system_id.code or "0",
                    post_slaughter_system=rec.unece_meat_post_slaughter_system_id.code
                    or "0",
                    fat_thickness=rec.unece_meat_fat_thickness_id.code or "0",
                    quality_system=rec.unece_meat_bovine_quality_system_id.code or "0",
                    weight_range=rec.unece_meat_weight_range_id.code or "0",
                    packing=rec.unece_meat_packing_id.code or "0",
                    conformity_assessment=rec.unece_meat_conformity_assessment_id.code
                    or "0",
                )
            )
