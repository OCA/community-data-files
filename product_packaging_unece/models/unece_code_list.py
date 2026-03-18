# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class UneceCodeList(models.Model):

    _inherit = "unece.code.list"

    type = fields.Selection(
        selection_add=[("packaging_type", "Packaging Types (UNECE Rec 21)")],
        ondelete={"packaging_type": "cascade"},
    )
