# Copyright 2017 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    bank_code_ids = fields.One2many(
        comodel_name="res.bank.code",
        inverse_name="bank_id",
        string="Codes",
    )
