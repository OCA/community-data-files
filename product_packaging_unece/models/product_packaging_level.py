# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import api, fields, models
from odoo.tools import ormcache


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

    @api.model
    @ormcache()
    def _get_packaging_level_ids_by_unece_code(self):
        res = defaultdict(list)
        for level in self.search([("unece_type_ids", "!=", False)]):
            for unece_type in level.unece_type_ids:
                res[unece_type.code].append(level.id)
        return res

    def get_packaging_level_ids_for_codes(self, *unece_codes):
        mapping = self._get_packaging_level_ids_by_unece_code()
        if len(unece_codes) == 1 and isinstance(unece_codes[0], (list, tuple, set)):
            unece_codes = unece_codes[0]
        return [lid for code in unece_codes for lid in mapping.get(code, [])]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        self._get_packaging_level_ids_by_unece_code.clear_cache(self)
        return records

    def write(self, vals):
        res = super().write(vals)
        self._get_packaging_level_ids_by_unece_code.clear_cache(self)
        return res

    def unlink(self):
        res = super().unlink()
        self._get_packaging_level_ids_by_unece_code.clear_cache(self)
        return res
