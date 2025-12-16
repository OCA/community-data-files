# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class AdrPackagingType(models.Model):
    _name = "adr.packaging.type"
    _description = "ADR Packaging"

    name = fields.Char(required=True)
