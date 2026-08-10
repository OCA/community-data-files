# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TradeComplianceRegime(models.Model):
    _name = "trade.compliance.regime"
    _description = "Trade Compliance Regime"
    _order = "name"

    name = fields.Char(
        required=True,
        help="Short name of the regime (e.g., US-EAR, EU-DUAL)",
    )
    description = fields.Text(
        help="Description of the authority and regulatory framework",
    )
    active = fields.Boolean(
        default=True,
        help="Uncheck to archive this regime",
    )

    _sql_constraints = [
        (
            "name_unique",
            "unique(name)",
            "A compliance regime with this name already exists",
        )
    ]
