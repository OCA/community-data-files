# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2022,2024 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo.tests import Form, common


class TestBaseBankFromIban(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        partner_bank = Form(self.bank_obj)
        partner_bank.acc_number = "es1299999999509999999999"
        self.assertEqual(partner_bank.acc_number, "ES12 9999 9999 5099 9999 9999")
        self.assertEqual(partner_bank.bank_id, self.bank)

    def test_onchange_acc_number_no_iban(self):
        partner_bank = Form(self.bank_obj)
        partner_bank.acc_number = "es1299999999509999999999x"
        self.assertFalse(partner_bank.bank_id)

    def test_onchange_acc_number_iban_wizard(self):
        wizard = Form(self.env["account.setup.bank.manual.config"])
        wizard.acc_number = "99999999509999999999"
        self.assertFalse(wizard.bank_id)
        wizard.acc_number = "ES1299999999509999999999"
        self.assertEqual(wizard.acc_number, "ES12 9999 9999 5099 9999 9999")
        self.assertEqual(wizard.bank_id, self.bank)
        wizard.acc_number = ""
        self.assertEqual(wizard.bank_id, self.bank)

    def test_create_iban_not_found(self):
        partner_bank = self.env["res.partner.bank"].create(
            {"acc_number": "es1299999999509999999999", "partner_id": self.partner.id}
        )
        self.assertFalse(partner_bank.bank_id)

    def test_create_iban_found(self):
        partner_bank = self.env["res.partner.bank"].create(
            {"acc_number": "DE89370400440532013000", "partner_id": self.partner.id}
        )
        self.assertTrue(partner_bank.bank_id)
        self.assertTrue(partner_bank.bank_id.name, "Commerzbank")
        self.assertTrue(partner_bank.bank_id.bic, "COBADEFFXXX")
        self.assertTrue(partner_bank.bank_id.code, "37040044")
        self.assertTrue(partner_bank.bank_id.country.code, "DE")

    def test_create_iban_found_existing_bank(self):
        bank = self.env["res.bank"].create(
            {
                "country": self.env.ref("base.de").id,
                "code": "37040044",
                "name": "Commerzbank",
            }
        )
        partner_bank = self.env["res.partner.bank"].create(
            {"acc_number": "DE89370400440532013000", "partner_id": self.partner.id}
        )
        self.assertEqual(partner_bank.bank_id, bank)
        self.assertTrue(bank.bic, "COBADEFFXXX")

    def test_create_invalid_iban(self):
        partner_bank = self.env["res.partner.bank"].create(
            {"acc_number": "1234567890", "partner_id": self.partner.id}
        )
        # The important thing here is to not see any warning in the log
        self.assertTrue(partner_bank)
