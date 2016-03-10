# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestBaseBicFromIban(TransactionCase):
    def test_base_bic_from_iban(self):
        bank_account = self.env['res.partner.bank'].new({
            'state': 'iban',
            'acc_number': 'NL42TRIO4242424242',
        })
        bank_account.onchange_acc_number()
        self.assertEqual(
            bank_account.bank_bic or bank_account.bank.bic, 'TRIONL2U')
