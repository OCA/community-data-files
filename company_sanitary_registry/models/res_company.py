# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sanitary_registry_id = fields.Many2one("sanitary.registry")
    # Field to avoid crashes modules that uses yet this field. To be removed
    # On future versions.
    sanitary_registry = fields.Char(related="sanitary_registry_id.name")
