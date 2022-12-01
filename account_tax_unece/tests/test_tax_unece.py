# Copyright 2017-2020 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2019-2020 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestTaxUnece(HttpCase):
    def test_get_tax_vals(self):
        tax_templates = self.env["account.tax.template"].search([])
        for template in tax_templates:
            template.unece_type_id = self.env.ref("account_tax_unece.tax_type_aaa")
            template.unece_categ_id = self.env.ref("account_tax_unece.tax_categ_a")
            res = template._get_tax_vals(self.env.company, {})
            self.assertTrue(res["unece_type_id"])
            self.assertTrue(res["unece_categ_id"])
            template.unece_type_id = False
            template.unece_categ_id = False
            res = template._get_tax_vals(self.env.company, {})
            self.assertFalse(res["unece_type_id"])
            self.assertFalse(res["unece_categ_id"])

    def test_company_speeddict_methods(self):
        company = self.env.ref("base.main_company")
        res_tax = company._get_tax_unece_speeddict()
        self.assertTrue(isinstance(res_tax, dict))
        res_fp = company._get_fiscal_position_speeddict("en_US")
        self.assertTrue(isinstance(res_fp, dict))
