# -*- coding: utf-8 -*-
# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestBaseIso3166(common.TransactionCase):
    def test_iso_3166(self):
        country = self.env.ref('base.ad')
        self.assertEqual(country.code_alpha3, 'AND')
        self.assertEqual(country.code_numeric, '020')
