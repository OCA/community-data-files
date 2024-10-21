# Copyright 2021 Stefan Rijnhart <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.osv.expression import AND


class AdrClass(models.Model):
    _name = "adr.class"
    _description = "Dangerous Goods Class"
    _order = "code, name"

    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """Allow to search for full codes"""
        args = list(args or [])
        if name and operator in ("ilike", "="):
            res = self.search(AND([args, [("code", operator, name)]]), limit=limit)
            if res:
                return [(rec.id, rec.display_name) for rec in res]
        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    @api.depends("code", "name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.code} {record.name}"

    _sql_constraints = [
        (
            "code_unique",
            "unique(code)",
            "A dangerous goods class with this code already exists",
        )
    ]
