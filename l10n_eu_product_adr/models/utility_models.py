# Copyright 2020 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class UnReference(models.Model):
    _name = "un.reference"
    _description = "UN Reference"

    name = fields.Char(string="Code", required=True)
    description = fields.Char(string="Description", required=True, translate=True)

    _sql_constraints = [
        ("un_name_unique", "unique(name)", "This description already exist"),
        (
            "un_description_unique",
            "unique(description)",
            "This description already exist",
        ),
    ]

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("description", operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "{} {}".format(rec.name, rec.description)))
        return res


class DangerousUOM(models.Model):
    _name = "dangerous.uom"
    _description = "Dangerous UOM"

    name = fields.Char(string="Name", required=True, translate=True)


class Great(models.Model):
    _name = "great.class"
    _description = "Great"

    name = fields.Char(string="Name", required=True)


class LimitedAmount(models.Model):
    _name = "limited.amount"
    _description = "Limited Amount"

    name = fields.Char(string="Name", required=True)


class StorageClass(models.Model):
    _name = "storage.class"
    _description = "Storage class"

    name = fields.Char(string="Name", required=True)


class PackaginType(models.Model):
    _name = "packaging.type"
    _description = "Packaging"

    name = fields.Char(string="Name", required=True)


class StorageTemp(models.Model):
    _name = "storage.temp"
    _description = "Storage Temp"

    name = fields.Char(string="Name", required=True, translate=True)


class DangerousGoods(models.Model):
    _name = "dangerous.goods"
    _description = "Dangerous Goods"

    name = fields.Char(string="Name", required=True)


class WGKClass(models.Model):
    _name = "wgk.class"
    _description = "WGK class"

    name = fields.Char(string="Name", required=True)
