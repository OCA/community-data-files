# Copyright 2019 Camptocamp SA
# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class StockMove(models.Model):
    _inherit = "stock.move"

    adr_points = fields.Float(
        compute="_compute_adr_points",
        string="ADR Points",
        digits="Product Unit of Measure",
        compute_sudo=True,
    )

    @api.depends("product_id", "product_uom_qty")
    def _compute_adr_points(self):
        """Compute the normalized ADR points

        Set the ADR points for the weight or quantity of the given moves,
        multiplied by the factor derived from their UN number or transport category.
        """
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for sm in self:
            if not sm.product_id.adr_goods_id:
                sm.adr_points = 0
                continue
            if sm.product_id.weight:
                # Assume that the product weight is in kilos per unit
                reference_qty = sm.product_id.weight * sm.product_uom_qty
            else:
                # Conflate the reference unit (kilo, liter) with the ADR unit
                reference_qty = sm.product_uom_qty / sm.product_uom.factor
            sm.adr_points = float_round(
                sm.product_id.adr_factor * reference_qty, precision
            )
