# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class AdrStorageTemp(models.Model):
    _name = "adr.storage.temp"
    _description = "ADR Storage Temp"

    name = fields.Char(required=True, translate=True)
