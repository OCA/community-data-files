# Copyright 2017-2020 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2019-2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import HttpCase


class TestTaxUnece(HttpCase):
    def test_exigibility(self):
        tax_obj = self.env["account.tax"]
        for tax_exigibility in ("on_invoice", "on_payment"):
            unece_code = tax_obj._get_unece_code_from_tax_exigibility(tax_exigibility)
            res_tax_exigibility = tax_obj._get_tax_exigibility_from_unece_code(
                unece_code
            )
            self.assertEqual(tax_exigibility, res_tax_exigibility)
