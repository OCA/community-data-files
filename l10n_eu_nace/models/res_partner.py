# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = 'res.partner'

    nace_id = fields.Many2one(
        comodel_name="res.partner.nace", string="NACE", index=True
    )
