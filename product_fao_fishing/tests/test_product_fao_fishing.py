# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError
from odoo.tests import SavepointCase


class TestProductFaoFishing(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_attribute = cls.env.ref("product_fao_fishing.fao_fishing_area")
        cls.product_attribute_value_1 = cls.env.ref(
            "product_fao_fishing.fao_fishing_area_1"
        )
        cls.product_attribute_value_2 = cls.env.ref(
            "product_fao_fishing.fao_fishing_area_2"
        )
        cls.product = cls.env["product.template"].create(
            {
                "name": "test",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.product_attribute.id,
                            "value_ids": [
                                (4, cls.product_attribute_value_1.id),
                                (4, cls.product_attribute_value_2.id),
                            ],
                        },
                    )
                ],
            }
        )
        cls.fishing_tech_arrow = cls.env.ref(
            "product_fao_fishing.fishing_technique_harrows"
        )
        cls.my_tech = cls.env["product.fao.fishing.technique"].create(
            {"name": "My Tech", "parent_id": cls.fishing_tech_arrow.id}
        )

    def test_fishing_technique_name(self):
        self.assertEqual(
            self.my_tech.complete_name,
            "{} / {}".format(self.fishing_tech_arrow.name, self.my_tech.name),
        )

    def test_recursion(self):
        with self.assertRaises(UserError):
            self.my_tech.parent_id = self.my_tech

    def test_fishing_areas_from_attribute(self):
        """
        Test helper method to access directly to FAO fishing area product
        """
        self.assertEqual(len(self.product.fao_fishing_area_ids), 2)
