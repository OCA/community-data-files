# Copyright 2021 Stefan Rijnhart <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class AdrClass(models.Model):
    _name = "adr.class"
    _description = "Dangerous Goods Class"
    _order = "code, name"
    _rec_names_search = ["name", "code"]

    code = fields.Char(required=True)
    name = fields.Char(required=True, translate=True)

    @api.depends("code", "name")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.code} {record.name}"

    _code_unique = models.Constraint(
        "unique(code)",
        "A dangerous goods class with this code already exists",
    )
