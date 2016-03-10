# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.onchange('acc_number')
    def onchange_acc_number(self):
        """Look up the IBAN's BIC and select the proper bank. If not found,
        just set the BIC"""
        if self.state != 'iban':
            return
        iban = self.acc_number
        if 'sanitized_acc_number' in self._fields:
            iban = self.sanitized_acc_number
        bic = self.env['res.bank.iban.bic.mapping'].lookup_bic(iban)
        if not bic:
            return
        bank = self.env['res.bank'].search([('bic', '=', bic)], limit=1)
        if not bank:
            self.bank_bic = bic
        else:
            self.bank = bank
