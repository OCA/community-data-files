# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class AdrWGKClass(models.Model):
    _name = "adr.wgk.class"
    _description = "ADR WGK Class"

    name = fields.Char(required=True)
