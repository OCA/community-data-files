# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.exceptions import ValidationError
from odoo.tests import SavepointCase


class TestAdrModels(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.lang = "en_US"

    def test_01_adr_class(self):
        """Test adr.class name_search and name_get"""
        adr_class = self.env["adr.class"].create(
            {
                "code": "test_code",
                "name": "test name",
            }
        )
        self.assertEqual(
            self.env["adr.class"].name_search("test_code"),
            [(adr_class.id, "test_code test name")],
        )
        self.assertEqual(
            self.env["adr.class"].name_search("est nam"),
            [(adr_class.id, "test_code test name")],
        )

    def test_02_adr_goods(self):
        """Test adr.goods validations, name_search, name_get"""
        adr_goods = self.env["adr.goods"].create(
            {
                "un_number": "9999",
                "name": "test goods",
                "class_id": self.env.ref("l10n_eu_product_adr.adr_class_1").id,
                "transport_category": "-",
                "tunnel_restriction_code": "-",
            }
        )
        with self.assertRaisesRegex(
            ValidationError, "length of 4"
        ), self.env.clear_upon_failure():
            adr_goods.un_number = "999"

        self.assertEqual(
            self.env["adr.goods"].name_search("9999"),
            [(adr_goods.id, "9999 test goods")],
        )
        self.assertEqual(
            self.env["adr.goods"].name_search("est goo"),
            [(adr_goods.id, "9999 test goods")],
        )
        adr_goods.transport_category = "4"
        self.assertEqual(
            adr_goods.name_get(), [(adr_goods.id, "9999 test goods (cat:4)")]
        )
        adr_goods.write(
            {
                "limited_quantity": 5,
                "limited_quantity_uom_id": self.env.ref(
                    "l10n_eu_product_adr.product_uom_mililiter"
                ).id,
            }
        )
        self.assertEqual(
            adr_goods.name_get(),
            [(adr_goods.id, "9999 test goods (cat:4, qty:5.0 ml)")],
        )

    def test_03_adr_label(self):
        """Labels that are in use cannot be deleted"""
        label = self.env.ref("l10n_eu_product_adr.adr_label_1").copy()
        goods = self.env.ref("l10n_eu_product_adr.adr_goods_0066")
        goods.label_ids += label
        with self.assertRaisesRegex(ValidationError, "in use"):
            label.unlink()
        goods.label_ids -= label
        label.unlink()
