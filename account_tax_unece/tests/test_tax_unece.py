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
