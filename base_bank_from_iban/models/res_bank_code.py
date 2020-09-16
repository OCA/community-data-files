# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResBankCode(models.Model):

    _name = 'res.bank.code'
    _description = 'Res Bank Code'
    _rec_name = 'code'

    code = fields.Char(required=True)
    bank_id = fields.Many2one(
        comodel_name="res.bank", string="Bank", required=True
    )
