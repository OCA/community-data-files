# Copyright 2017 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# Copyright 2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo.tests import Form, common


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

        # support for IBAN's with bic instead of code
        cls.country_netherlands = cls.env.ref("base.nl")
        cls.bank_ing = cls.env["res.bank"].create(
            {
                "name": "ING BANK NETHERLANDS",
                "code": "",
                "bic": "INGBNL2A",
                "country": cls.country_netherlands.id,
            }
        )
        cls.partner_nl = cls.env["res.partner"].create(
            {
                "name": "Roverheid",
                "country_id": cls.country_netherlands.id,
            }
        )
        cls.bank_obj_nl = cls.env["res.partner.bank"].with_context(
            default_partner_id=cls.partner_nl.id
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

    def test_onchange_acc_number_iban_wizard(self):
        wizard = Form(self.env["account.setup.bank.manual.config"])
        wizard.acc_number = "99999999509999999999"
        self.assertFalse(wizard.bank_id)
        wizard.acc_number = "ES1299999999509999999999"
        self.assertEqual(wizard.acc_number, "ES12 9999 9999 5099 9999 9999")
        self.assertEqual(wizard.bank_id, self.bank)
        wizard.acc_number = ""
        self.assertEqual(wizard.bank_id, self.bank)

    def test_onchange_acc_number_iban_from_bic(self):
        partner_bank = self.bank_obj.new()
        partner_bank.acc_number = "nl36ingb0003445588"
        partner_bank._onchange_acc_number_base_bank_from_iban()
        self.assertEqual(partner_bank.acc_number, "NL36 INGB 0003 4455 88")
        self.assertEqual(partner_bank.bank_id, self.bank_ing)
