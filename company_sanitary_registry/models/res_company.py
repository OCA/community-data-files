# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sanitary_registry = fields.Char()
