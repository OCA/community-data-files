# Copyright 2017-2020 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2019-2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests.common import HttpCase


class TestTaxUnece(HttpCase):
    def test_company_speeddict_methods(self):
        company = self.env.ref("base.main_company")
        res_tax = company._get_tax_unece_speeddict()
        self.assertTrue(isinstance(res_tax, dict))
        res_fp = company._get_fiscal_position_speeddict("en_US")
        self.assertTrue(isinstance(res_fp, dict))
