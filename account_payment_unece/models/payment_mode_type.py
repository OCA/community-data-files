# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PaymentModeType(models.Model):
    _inherit = 'payment.mode.type'

    unece_id = fields.Many2one(
        'unece.code.list', string='UNECE Payment Mean',
        domain=[('type', '=', 'payment_means')],
        help="Standard nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE) defined in UN/EDIFACT Data "
        "Element 4461")
    unece_code = fields.Char(
        related='unece_id.code', store=True, string='UNECE Code')
