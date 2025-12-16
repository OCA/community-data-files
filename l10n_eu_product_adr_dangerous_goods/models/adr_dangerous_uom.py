# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class AdrDangerousUOM(models.Model):
    _name = "adr.dangerous.uom"
    _description = "ADR Dangerous UOM"

    name = fields.Char(required=True, translate=True)
