# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import ormcache


class UomUom(models.Model):
    _inherit = "uom.uom"

    unece_code = fields.Char(
        string="UNECE Code",
        help="Standard nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE).",
    )

    @api.model
    @ormcache()
    def _get_uom_id_by_unece_code(self):
        uoms = self.search([("unece_code", "!=", False)])
        return {u.unece_code: u.id for u in uoms}

    def get_uom_id_by_unece_code(self, unece_code):
        uom_ids_by_code = self._get_uom_id_by_unece_code()
        return uom_ids_by_code.get(unece_code)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if records.filtered("unece_code"):
            self._get_uom_id_by_unece_code.clear_cache(self)
        return records

    def write(self, vals):
        res = super().write(vals)
        if "unece_code" in vals:
            self._get_uom_id_by_unece_code.clear_cache(self)
        return res

    def unlink(self):
        res = super().unlink()
        self._get_uom_id_by_unece_code.clear_cache(self)
        return res
