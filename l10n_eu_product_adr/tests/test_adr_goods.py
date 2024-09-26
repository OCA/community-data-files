# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase


class TestAdrModels(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.lang = "en_US"
        cls.size_attr = cls.env["product.attribute"].create({"name": "Size"})
        cls.value_s = cls.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": cls.size_attr.id}
        )
        cls.value_m = cls.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": cls.size_attr.id}
        )
        cls.value_l = cls.env["product.attribute.value"].create(
            {"name": "L", "attribute_id": cls.size_attr.id}
        )
        cls.goods1 = cls.env.ref("l10n_eu_product_adr.adr_goods_0065")
        cls.goods2 = cls.env.ref("l10n_eu_product_adr.adr_goods_0066")

    def test_01_adr_class(self):
        """Test adr.class name_search and display_name"""
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
        """Test adr.goods validations, name_search, display_name"""
        adr_goods = self.env["adr.goods"].create(
            {
                "un_number": "9999",
                "name": "test goods",
                "class_id": self.env.ref("l10n_eu_product_adr.adr_class_1").id,
                "transport_category": "-",
                "tunnel_restriction_code": "-",
            }
        )
        with (
            self.assertRaisesRegex(ValidationError, "length of 4"),
            self.env.cr.savepoint(),
        ):
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
        self.assertEqual(adr_goods.display_name, "9999 test goods (cat:4)")
        adr_goods.write(
            {
                "limited_quantity": 5,
                "limited_quantity_uom_id": self.env.ref(
                    "l10n_eu_product_adr.product_uom_mililiter"
                ).id,
            }
        )
        self.assertEqual(
            adr_goods.display_name,
            "9999 test goods (cat:4, qty:5.0 ml)",
        )

    def test_03_adr_label(self):
        """Labels that are in use cannot be deleted"""
        label = self.env.ref("l10n_eu_product_adr.adr_label_1").copy()
        self.goods1.label_ids += label
        with self.assertRaisesRegex(ValidationError, "in use"):
            label.unlink()
        self.goods1.label_ids -= label
        label.unlink()

    def test_04_product_variant_write(self):
        """It is possible to configure the adr settings per variant"""
        template = self.env["product.template"].create(
            {
                "name": "Sofa",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.size_attr.id,
                            "value_ids": [(4, self.value_s.id), (4, self.value_m.id)],
                        },
                    ),
                ],
            }
        )
        var1, var2 = template.product_variant_ids
        self.assertFalse(template.adr_goods_on_variants)
        var1.adr_goods_id = self.goods1
        self.assertTrue(template.adr_goods_on_variants)
        self.assertFalse(var2.adr_goods_id)
        var2.adr_goods_id = self.goods2
        self.assertTrue(template.adr_goods_on_variants)
        self.assertEqual(var1.adr_classification_code, "1.1D")
        self.assertEqual(var2.adr_classification_code, "1.4G")
        var1.adr_goods_id = self.goods2
        self.assertFalse(template.adr_goods_on_variants)
        template.adr_goods_id = self.goods1
        self.assertEqual(var1.adr_goods_id, self.goods1)
        self.assertEqual(var2.adr_goods_id, self.goods1)
        var2.adr_goods_id = False
        self.assertTrue(template.adr_goods_on_variants)
        with self.assertRaisesRegex(UserError, "variant"):
            template.adr_goods_id = self.goods1
        var1.adr_goods_id = False
        template.adr_goods_id = self.goods1
        template.adr_goods_id = False
        self.assertFalse(var1.adr_goods_id)
        self.assertFalse(var2.adr_goods_id)

    def test_05_product_variant_create(self):
        """Variants are initialized with the settings of the template"""
        template = self.env["product.template"].create(
            {
                "name": "Sofa",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.size_attr.id,
                            "value_ids": [(4, self.value_s.id), (4, self.value_m.id)],
                        },
                    ),
                ],
                "adr_goods_id": self.goods1.id,
                "is_dangerous": True,
            }
        )
        var1, var2 = template.product_variant_ids
        self.assertEqual(var1.adr_goods_id, self.goods1)
        self.assertEqual(var2.adr_goods_id, self.goods1)

        template.attribute_line_ids.value_ids += self.value_l
        self.assertEqual(len(template.product_variant_ids), 3)
        self.assertTrue(
            var.adr_goods_id == self.goods1 for var in template.product_variant_ids
        )
