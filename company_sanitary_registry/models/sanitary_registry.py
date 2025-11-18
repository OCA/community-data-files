# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SanitaryRegistry(models.Model):
    _name = "sanitary.registry"
    _description = "Sanitary Registry"

    name = fields.Char()

    @api.constrains("name")
    def _check_name(self):
        other_regs = self.env["sanitary.registry"].search(
            [("id", "not in", self.ids), ("name", "in", self.mapped("name"))]
        )
        if other_regs:
            raise ValidationError(
                _(
                    "There are already sanitary registrations with values %s.",
                    other_regs.mapped("name"),
                )
            )
