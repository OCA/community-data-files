# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResPartnerNace(TransactionCase):
    def setUp(self):
        super(TestResPartnerNace, self).setUp()
        self.nace = self.env['res.partner.nace'].create(
            {'name': 'nace_test', 'code': 'code_nace'}
        )

    def test_name_get(self):
        self.assertEqual(self.nace.name, 'nace_test')
        self.assertEqual(self.nace.display_name, '[code_nace] nace_test')

    def test_name_search(self):
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("code_nace"),
        )
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("nace_test"),
        )
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search(
                "code_nace", args=[("id", "=", self.nace.id)]
            ),
        )
        self.assertEquals(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("ode_nac"),
        )
        self.assertEquals(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("ace_te"),
        )
        self.assertEquals(
            self.nace.name_get(),
            self.env['res.partner.nace'].name_search(
                'nace_test', operator="="
            ),
        )
        self.assertEquals(
            self.nace.name_get(),
            self.env['res.partner.nace'].name_search(
                'code_nace', operator="="
            ),
        )
