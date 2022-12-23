# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2022 Tecnativa - Pedro M. Baeza
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
