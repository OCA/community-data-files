# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import AND


class TradeComplianceCode(models.Model):
    _name = "trade.compliance.code"
    _description = "Trade Compliance Code"
    _order = "regime_id, name"

    name = fields.Char(
        required=True,
        help="The compliance code (e.g., 3A001, EAR99)",
    )
    regime_id = fields.Many2one(
        comodel_name="trade.compliance.regime",
        string="Regime",
        required=True,
        ondelete="restrict",
        help="The regulatory regime this code belongs to",
    )
    description = fields.Text(
        help="Description of what this code controls",
    )
    active = fields.Boolean(
        default=True,
        help="Uncheck to archive outdated codes",
    )

    def name_get(self):
        """Override to show code with regime"""
        return [
            (
                rec.id,
                f"{rec.name} ({rec.regime_id.name})" if rec.regime_id else rec.name,
            )
            for rec in self
        ]

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """Search by code or regime name"""
        args = args or []
        if not name:
            return super().name_search(
                name=name, args=args, operator=operator, limit=limit
            )

        domain = [
            "|",
            "|",
            ("name", operator, name),
            ("description", operator, name),
            ("regime_id.name", operator, name),
        ]
        recs = self.search(AND([args, domain]), limit=limit)
        return recs.name_get()

    _sql_constraints = [
        (
            "name_regime_unique",
            "unique(name, regime_id)",
            "A compliance code with this name already exists for this regime",
        )
    ]
