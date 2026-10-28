# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2022,2024 Tecnativa - Pedro M. Baeza
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo.tests import Form, common


class TestBaseBankFromIban(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Tecnativa, S.L"})
        cls.bank_obj = cls.env["res.partner.bank"].with_context(
            default_partner_id=cls.partner.id
        )
        cls.iban = "DE89370400440532013000"

    def _create_account(self, **vals):
        return self.bank_obj.create(
            dict(account_number=self.iban, partner_id=self.partner.id, **vals)
        )

    def _assert_bank_details(self, account):
        self.assertEqual(account.bank_name, "Commerzbank")
        self.assertEqual(account.bank_bic, "COBADEFFXXX")
        self.assertEqual(account.country_id, self.env.ref("base.de"))

    def test_create_iban(self):
        self._assert_bank_details(self._create_account())

    def test_explicit_values_preserved(self):
        account = self._create_account(bank_name="Custom bank", bank_bic=False)
        self.assertEqual(account.bank_name, "Custom bank")
        self.assertFalse(account.bank_bic)
        self.assertEqual(account.country_id, self.env.ref("base.de"))

    def test_write_iban(self):
        account = self.bank_obj.create(
            {"account_number": "1234567890", "partner_id": self.partner.id}
        )
        account.write({"account_number": self.iban})
        self._assert_bank_details(account)
        account.write({"bank_name": "Custom bank"})
        self.assertEqual(account.bank_name, "Custom bank")

    def test_write_explicit_values_preserved(self):
        account = self._create_account()
        account.write({"account_number": self.iban, "bank_name": "Custom bank"})
        self.assertEqual(account.bank_name, "Custom bank")

    def test_create_multi(self):
        accounts = self.bank_obj.create(
            [
                {"account_number": self.iban, "partner_id": self.partner.id},
                {"account_number": "1234567890", "partner_id": self.partner.id},
            ]
        )
        self._assert_bank_details(accounts[0])
        self.assertFalse(accounts[1].bank_name)

    def test_onchange_iban(self):
        with Form(self.bank_obj) as account:
            account.account_number = self.iban.lower()
            self.assertEqual(account.account_number, "DE89 3704 0044 0532 0130 00")
            self._assert_bank_details(account)

    def test_onchange_non_iban(self):
        account = self.bank_obj.new({"account_number": "1234567890"})
        account._onchange_account_number_base_bank_from_iban()
        self.assertFalse(account.bank_name)
        self.assertFalse(account.bank_bic)

    def test_unknown_bank(self):
        account = self.bank_obj.create(
            {
                "account_number": "ES1299999999509999999999",
                "partner_id": self.partner.id,
            }
        )
        self.assertFalse(account.bank_name)
        self.assertFalse(account.bank_bic)
        self.assertEqual(account.country_id, self.env.ref("base.es"))

    def test_invalid_iban(self):
        for number in ("1234567890", "DE00370400440532013000", ""):
            self.assertEqual(self.bank_obj._get_bank_from_iban(number), {})

    def test_onchange_wizard(self):
        wizard = self.env["account.setup.bank.manual.config"].new(
            {"account_number": self.iban.lower()}
        )
        wizard._onchange_account_number_base_bank_from_iban()
        self.assertEqual(wizard.account_number, "DE89 3704 0044 0532 0130 00")
        self._assert_bank_details(wizard)
        wizard.account_number = False
        wizard._onchange_account_number_base_bank_from_iban()
        self._assert_bank_details(wizard)
