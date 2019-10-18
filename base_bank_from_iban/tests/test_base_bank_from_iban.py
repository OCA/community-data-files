# Copyright 2017 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo.tests import common


class TestBaseBankFromIban(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestBaseBankFromIban, cls).setUpClass()
        cls.country_spain = cls.env.ref("base.es")
        cls.bank = cls.env["res.bank"].create(
            {"name": "BDE", "code": "9999", "country": cls.country_spain.id}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Tecnativa, S.L",
                "vat": "ES12345678Z",
                "country_id": cls.country_spain.id,
            }
        )
        cls.bank_obj = cls.env["res.partner.bank"].with_context(
            default_partner_id=cls.partner.id
        )

    def test_onchange_acc_number_iban(self):
        partner_bank = self.bank_obj.new()
        partner_bank.acc_number = "es1299999999509999999999"
        partner_bank._onchange_acc_number_base_bank_from_iban()
        self.assertEqual(partner_bank.acc_number, "ES12 9999 9999 5099 9999 9999")
        self.assertEqual(partner_bank.bank_id, self.bank)

    def test_onchange_acc_number_no_iban(self):
        partner_bank = self.bank_obj.new()
        partner_bank.acc_number = "es1299999999509999999999x"
        partner_bank._onchange_acc_number_base_bank_from_iban()
        self.assertFalse(partner_bank.bank_id)

    def test_onchange_acc_number_iban_journal(self):
        journal = self.env["account.journal"].new()
        journal.bank_acc_number = "ES1299999999509999999999"
        journal._onchange_bank_acc_number_base_bank_from_iban()
        self.assertEqual(journal.bank_acc_number, "ES12 9999 9999 5099 9999 9999")
        self.assertEqual(journal.bank_id, self.bank)
        journal.bank_acc_number = ""
        journal._onchange_bank_acc_number_base_bank_from_iban()
        self.assertEqual(journal.bank_id, self.bank)

    def test_onchange_acc_number_no_iban_journal(self):
        journal = self.env["account.journal"].new()
        journal.bank_acc_number = "99999999509999999999"
        journal._onchange_bank_acc_number_base_bank_from_iban()
        self.assertFalse(journal.bank_id)
        journal.bank_acc_number = ""
        journal._onchange_bank_acc_number_base_bank_from_iban()
        self.assertFalse(journal.bank_id)
