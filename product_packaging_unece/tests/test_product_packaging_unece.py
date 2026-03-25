# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestProductPackagingUnece(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.level_model = cls.env["product.packaging.level"]
        cls.unece_bx = cls.env.ref("product_packaging_unece.unece_packaging_bx")
        cls.unece_ct = cls.env.ref("product_packaging_unece.unece_packaging_ct")
        cls.unece_pl = cls.env.ref("product_packaging_unece.unece_packaging_pl")

        cls.level_box = cls.level_model.create(
            {
                "name": "Box level",
                "code": "BX",
                "sequence": 1,
                "unece_type_ids": [Command.set([cls.unece_bx.id])],
            }
        )
        cls.level_carton_pallet = cls.level_model.create(
            {
                "name": "Carton/Pallet level",
                "code": "CA",
                "sequence": 2,
                "unece_type_ids": [Command.set([cls.unece_ct.id, cls.unece_pl.id])],
            }
        )
        cls.level_pallet = cls.level_model.create(
            {
                "name": "Pallet level",
                "code": "PL",
                "sequence": 3,
                "unece_type_ids": [Command.set([cls.unece_pl.id])],
            }
        )

    def test_get_packaging_level_ids_by_one_code(self):
        level_ids = self.level_model.get_packaging_level_ids_for_codes("BX")
        self.assertEqual(set(level_ids), {self.level_box.id})

    def test_get_packaging_level_ids_by_multiple_codes(self):
        level_ids = self.level_model.get_packaging_level_ids_for_codes("BX", "PL")
        self.assertEqual(
            set(level_ids),
            {self.level_box.id, self.level_carton_pallet.id, self.level_pallet.id},
        )

    def test_get_packaging_level_ids_by_list_of_codes(self):
        level_ids = self.level_model.get_packaging_level_ids_for_codes(["CT", "PL"])
        self.assertEqual(
            set(level_ids),
            {self.level_carton_pallet.id, self.level_pallet.id},
        )

    def test_get_packaging_level_ids_by_unknown_code(self):
        level_ids = self.level_model.get_packaging_level_ids_for_codes("XXX")
        self.assertEqual(level_ids, [])

    def test_get_packaging_level_ids_by_false_code(self):
        level_ids = self.level_model.get_packaging_level_ids_for_codes(False)
        self.assertEqual(level_ids, [])
