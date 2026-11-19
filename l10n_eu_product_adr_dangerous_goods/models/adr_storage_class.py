# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class AdrStorageClass(models.Model):
    _name = "adr.storage.class"
    _description = "ADR Storage Class"

    name = fields.Char(required=True)
