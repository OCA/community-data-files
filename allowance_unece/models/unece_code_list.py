# © 2020 Decodio Applications ltd (https://decod.io)
# @author: Davor Bojkic <davor.bojkic@decod.io>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields


class UneceCodeList(models.Model):
    _inherit = 'unece.code.list'

    type = fields.Selection(selection_add=[
        ('allowance', 'Allowance Types (UNCL 5189)'),
        ])
