# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.l10n_eu_product_adr.hooks import fill_adr_factor


class TestAdrFactor(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Transport category 1, no exception on the UN number: factor 50
        cls.goods_category_1 = cls.env.ref("l10n_eu_product_adr.adr_goods_0065")
        # Transport category 2: factor 3
        cls.goods_category_2 = cls.env.ref("l10n_eu_product_adr.adr_goods_0066")
        # Transport category 3: factor 1
        cls.goods_category_3 = cls.env.ref("l10n_eu_product_adr.adr_goods_1002")
        # Transport category 4: factor 0
        cls.goods_category_4 = cls.env.ref("l10n_eu_product_adr.adr_goods_0012")
        # Transport category not applicable: factor 0
        cls.goods_no_category = cls.env.ref("l10n_eu_product_adr.adr_goods_1043")
        # Transport category 1, but the UN number caps the factor at 20
        cls.goods_un_exception = cls.env.ref("l10n_eu_product_adr.adr_goods_0081")
        cls.product = cls.env["product.product"].create({"name": "ADR product"})

    def test_01_factor_per_transport_category(self):
        """The factor is derived from the transport category of the goods"""
        for goods, factor in (
            (self.goods_category_1, 50),
            (self.goods_category_2, 3),
            (self.goods_category_3, 1),
            (self.goods_category_4, 0),
            (self.goods_no_category, 0),
        ):
            with self.subTest(un_number=goods.un_number):
                self.product.adr_goods_id = goods
                self.assertEqual(self.product.adr_factor, factor)

    def test_02_un_number_takes_precedence(self):
        """An UN number in the exception map overrides the transport category"""
        self.assertEqual(self.goods_un_exception.transport_category, "1")
        self.product.adr_goods_id = self.goods_un_exception
        self.assertEqual(self.product.adr_factor, 20)

    def test_03_factor_without_goods(self):
        """A product that is not dangerous goods has no factor"""
        self.assertEqual(self.product.adr_factor, 0)
        self.product.adr_goods_id = self.goods_category_1
        self.assertEqual(self.product.adr_factor, 50)
        self.product.adr_goods_id = False
        self.assertEqual(self.product.adr_factor, 0)

    def test_04_factor_on_create(self):
        """The factor is computed on creation, without a further write"""
        product = self.env["product.product"].create(
            {"name": "Created dangerous", "adr_goods_id": self.goods_category_2.id}
        )
        self.assertEqual(product.adr_factor, 3)

    def test_05_factor_is_editable(self):
        """The computed factor can be overridden by hand"""
        self.product.adr_goods_id = self.goods_category_2
        self.product.adr_factor = 7
        self.assertEqual(self.product.adr_factor, 7)
        # Only a change of the goods recomputes it
        self.product.adr_goods_id = self.goods_category_3
        self.assertEqual(self.product.adr_factor, 1)

    def test_06_variant_inherits_factor(self):
        """Variants created from a template get the factor of its goods"""
        attribute = self.env["product.attribute"].create({"name": "Size"})
        values = self.env["product.attribute.value"].create(
            [
                {"name": "S", "attribute_id": attribute.id},
                {"name": "M", "attribute_id": attribute.id},
            ]
        )
        template = self.env["product.template"].create(
            {
                "name": "Dangerous sofa",
                "is_dangerous": True,
                "adr_goods_id": self.goods_category_1.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, values.ids)],
                        },
                    )
                ],
            }
        )
        self.assertEqual(len(template.product_variant_ids), 2)
        for variant in template.product_variant_ids:
            self.assertEqual(variant.adr_factor, 50)

    def test_07_fill_adr_factor(self):
        """The SQL filling reproduces what the compute method returns"""
        products = self.env["product.product"].create(
            [
                {"name": "SQL 1", "adr_goods_id": self.goods_category_1.id},
                {"name": "SQL 2", "adr_goods_id": self.goods_un_exception.id},
                {"name": "SQL 3", "adr_goods_id": self.goods_no_category.id},
                {"name": "SQL 4"},
            ]
        )
        self.env.flush_all()
        self.env.cr.execute(
            "UPDATE product_product SET adr_factor = 999 WHERE id IN %s",
            (tuple(products.ids),),
        )
        self.env.invalidate_all()
        fill_adr_factor(self.env.cr)
        self.env.invalidate_all()
        self.assertEqual(products.mapped("adr_factor"), [50, 20, 0, 999])
