# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class StorageClass(models.Model):
    _name = "storage.class"
    _description = "Storage class"

    name = fields.Char(required=True)


class PackagingType(models.Model):
    _name = "packaging.type"
    _description = "Packaging"

    name = fields.Char(required=True)


class StorageTemp(models.Model):
    _name = "storage.temp"
    _description = "Storage Temp"

    name = fields.Char(required=True, translate=True)


class WGKClass(models.Model):
    _name = "wgk.class"
    _description = "WGK class"

    name = fields.Char(required=True)


class LimitedAmount(models.Model):
    _name = "limited.amount"
    _description = "Limited Amount"

    name = fields.Char(required=True)


class DangerousUOM(models.Model):
    _name = "dangerous.uom"
    _description = "Dangerous UOM"

    name = fields.Char(required=True, translate=True)
