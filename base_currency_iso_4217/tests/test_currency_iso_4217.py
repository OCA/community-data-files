# Copyright 2026 ForgeFlow, S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

# (xml id, full name, numeric code) as published by the ISO 4217 standard.
ISO_4217_SAMPLE = [
    ("base.EUR", "Euro", "978"),
    ("base.USD", "US Dollar", "840"),
    ("base.CHF", "Swiss Franc", "756"),
    # Numeric codes below 100 are padded with leading zeros.
    ("base.ALL", "Lek", "008"),
]


class TestCurrencyIso4217(TransactionCase):
    def test_iso_4217_data_loaded(self):
        """Currencies shipped by `base` get their ISO 4217 name and code."""
        for xml_id, full_name, numeric_code in ISO_4217_SAMPLE:
            currency = self.env.ref(xml_id)
            with self.subTest(currency=xml_id):
                self.assertEqual(currency.full_name, full_name)
                self.assertEqual(currency.numeric_code, numeric_code)

    def test_full_name_is_translatable(self):
        """The ISO name can be translated, unlike the one provided by `base`."""
        self.assertTrue(self.env["res.currency"]._fields["full_name"].translate)

    def test_views_show_a_single_full_name(self):
        """`base` already shows `full_name`, this module must not duplicate it."""
        currency_model = self.env["res.currency"]
        for xml_id, view_type in [
            ("base.view_currency_tree", "list"),
            ("base.view_currency_form", "form"),
        ]:
            arch = currency_model.get_view(self.env.ref(xml_id).id, view_type)["arch"]
            with self.subTest(view=xml_id):
                self.assertEqual(arch.count('name="full_name"'), 1)
                self.assertEqual(arch.count('name="numeric_code"'), 1)
