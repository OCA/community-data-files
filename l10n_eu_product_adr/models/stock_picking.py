# Copyright 2019 Camptocamp SA
# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    adr_points = fields.Float(
        compute="_compute_adr_points",
        string="ADR Points",
        digits="Product Unit of Measure",
    )

    @api.depends("move_lines.product_id", "move_lines.product_uom_qty")
    def _compute_adr_points(self):
        for picking in self:
            picking.adr_points = sum(sm.adr_points for sm in picking.move_lines)
