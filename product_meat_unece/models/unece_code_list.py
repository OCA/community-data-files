# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class UneceCodeList(models.Model):
    _inherit = "unece.code.list"

    type = fields.Selection(
        selection_add=[
            ("meat_species", "Species"),
            ("meat_product_cut", "Product/cut"),
            ("meat_refrigeration", "Refrigeration"),
            ("meat_bovine_category", "Bovine category"),
            ("meat_production_system", "Production system"),
            ("meat_feeding_system", "Feeding system"),
            ("meat_slaughter_system", "Slaughter system"),
            ("meat_post_slaughter_system", "Post-slaughter system"),
            ("meat_fat_thickness", "Fat thickness"),
            ("meat_bovine_quality_system", "Bovine quality system"),
            ("meat_weight_range", "Weight range"),
            ("meat_packing", "Packing"),
            ("meat_conformity_assessment", "Conformity assessment"),
        ]
    )

    @api.model
    def _get_unece_meat_code_length(self):
        """
        Defines the code length for each UNECE meat code type. This method is
        intended to be overridden.
        """
        return {
            "meat_species": 2,
            "meat_product_cut": 4,
            "meat_refrigeration": 1,
            "meat_bovine_category": 1,
            "meat_production_system": 1,
            "meat_feeding_system": 1,
            "meat_slaughter_system": 1,
            "meat_post_slaughter_system": 1,
            "meat_fat_thickness": 1,
            "meat_bovine_quality_system": 1,
            "meat_weight_range": 1,
            "meat_packing": 1,
            "meat_conformity_assessment": 1,
        }

    @api.constrains("type", "code")
    def _check_unece_meat_code_length(self):
        """
        Checks if the UNECE meat code matches exactly the required code length.
        """
        unece_meat_code_lengths = self._get_unece_meat_code_length()
        for rec in self:
            if rec.type not in unece_meat_code_lengths:
                continue
            required_code_length = unece_meat_code_lengths.get(rec.type)
            if len(rec.code) != required_code_length:
                raise ValidationError(
                    _(
                        'The code "{code}" doesn\'t match the required code length for '
                        "this type ({required_length})."
                    ).format(code=rec.code, required_length=required_code_length)
                )
