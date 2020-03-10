# Copyright 2016 Akretion (http://www.akretion.com)
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

    @api.depends("code", "name")
    def _compute_display_name(self):
        for entry in self:
            entry.display_name = "[{}] {}".format(entry.code, entry.name)

    code = fields.Char(required=True, copy=False)
    name = fields.Char(required=True, copy=False)
    display_name = fields.Char(compute="_compute_display_name", store=True)
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

    def name_get(self):
        res = []
        for entry in self:
            res.append((entry.id, "[{}] {}".format(entry.code, entry.name)))
        return res
