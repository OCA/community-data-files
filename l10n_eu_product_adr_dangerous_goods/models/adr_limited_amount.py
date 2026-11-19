# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class AdrLimitedAmount(models.Model):
    _name = "adr.limited.amount"
    _description = "ADR Limited Amount"

    name = fields.Char(required=True)
