# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestUomUnece(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_model = cls.env["uom.uom"]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.uom_hour = cls.env.ref("uom.product_uom_hour")

    def test_get_uom_id_by_unece_code(self):
        self.assertEqual(
            self.uom_model.get_uom_id_by_unece_code("C62"), self.uom_unit.id
        )
        self.assertEqual(
            self.uom_model.get_uom_id_by_unece_code("DPC"), self.uom_dozen.id
        )
        self.assertEqual(
            self.uom_model.get_uom_id_by_unece_code("HUR"), self.uom_hour.id
        )

    def test_get_uom_id_by_unece_code_unknown(self):
        self.assertFalse(self.uom_model.get_uom_id_by_unece_code("UNKNOWN"))

    def test_get_uom_id_by_unece_code_cache_invalidation_on_write(self):
        self.assertEqual(
            self.uom_model.get_uom_id_by_unece_code("C62"), self.uom_unit.id
        )
        self.uom_unit.write({"unece_code": "C62_NEW"})
        self.assertFalse(self.uom_model.get_uom_id_by_unece_code("C62"))
        self.assertEqual(
            self.uom_model.get_uom_id_by_unece_code("C62_NEW"), self.uom_unit.id
        )

    def test_get_uom_id_by_unece_code_cache_invalidation_on_unlink(self):
        uom = self.uom_hour.copy({"name": "Test Hour Copy", "unece_code": "ZZZ"})
        self.assertEqual(self.uom_model.get_uom_id_by_unece_code("ZZZ"), uom.id)
        uom.unlink()
        self.assertFalse(self.uom_model.get_uom_id_by_unece_code("ZZZ"))
