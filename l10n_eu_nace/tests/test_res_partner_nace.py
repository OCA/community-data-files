# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResPartnerNace(TransactionCase):
    def setUp(self):
        super(TestResPartnerNace, self).setUp()
        self.nace = self.env["res.partner.nace"].create(
            {"name": "nace_test", "code": "code_nace"}
        )
        self.child_nace = self.env["res.partner.nace"].create(
            {
                "name": "nace_child",
                "code": "code_child",
                "parent_id": self.nace.id,
            }
        )

    def test_complete_name_1(self):
        self.assertEqual(self.nace.name, "nace_test")
        self.assertEqual(self.nace.complete_name, "[code_nace] nace_test")
        self.assertEqual(
            self.child_nace.complete_name,
            "[code_child] nace_child",
        )

    def test_complete_name_2(self):
        self.assertEqual(
            self.child_nace.with_context(nace_display="long").complete_name,
            "[code_nace] nace_test / [code_child] nace_child",
        )

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
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("ode_nac"),
        )
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("ace_te"),
        )
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("nace_test", operator="="),
        )
        self.assertEqual(
            self.nace.name_get(),
            self.env["res.partner.nace"].name_search("code_nace", operator="="),
        )
