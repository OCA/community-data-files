# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

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
    def _compute_display_name(self):
        for entry in self:
            entry.display_name = f"[{entry.code}] {entry.name}"

    # _rec_names_search = ['name', 'code'] doesn't give the result we want
    # We want that, when you type an exact code, you get only that code
    # Exemple : on UNECE Tax category, when you type "S", you should get only
    # "[S] Standard rate"
    @api.model
    def _search_display_name(self, operator, value):
        if value and operator == "ilike":
            ids = list(self._search([("code", "=", value)]))
            if ids:
                return [("id", "in", ids)]
        return super()._search_display_name(operator, value)
