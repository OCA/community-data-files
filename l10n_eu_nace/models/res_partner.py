# Copyright 2019 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    primary_nace_id = fields.Many2one(
        'res.partner.nace', string="Primary NACE Activity")
    secondary_nace_ids = fields.Many2many(
        'res.partner.nace', string="Secondary NACE Activities")
