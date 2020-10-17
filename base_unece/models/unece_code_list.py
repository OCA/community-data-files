# Copyright 2016-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


# There are so many UNCL that can be usefull in Odoo
# that it would be stupid to have one object for each UNCL
# because it would duplicate the python code, views, menu entries, ACL, etc...
# So I decided to have a single object with a type field
class UneceCodeList(models.Model):
    _name = "unece.code.list"
    _description = "UNECE nomenclatures"
    _order = "type, code"

    code = fields.Char(required=True, copy=False)
    name = fields.Char(required=True, copy=False)
    type = fields.Selection([], required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "type_code_uniq",
            "unique(type, code)",
            "An UNECE code of the same type already exists",
        )
    ]

    @api.depends("code", "name")
    def name_get(self):
        res = []
        for entry in self:
            res.append((entry.id, "[{}] {}".format(entry.code, entry.name)))
        return res

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=80):
        if args is None:
            args = []
        if name and operator == "ilike":
            recs = self.search([("code", "=", name)] + args, limit=limit)
            if recs:
                return recs.name_get()
        return super().name_search(name=name, args=args, operator=operator, limit=limit)
