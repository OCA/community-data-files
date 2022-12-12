# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import SavepointCase


class TestProductFaoFishing(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_attribute = cls.env.ref("product_fao_fishing.fao_fishing_area")
        cls.fao_technique_attribute = cls.env.ref(
            "product_fao_fishing.fao_fishing_technique"
        )
        cls.product_attribute_value_1 = cls.env.ref(
            "product_fao_fishing.fao_fishing_area_1"
        )
        cls.product_attribute_value_2 = cls.env.ref(
            "product_fao_fishing.fao_fishing_area_2"
        )
        cls.technique_attribute_value_1 = cls.env.ref(
            "product_fao_fishing.fishing_technique_att_value_spearfishing"
        )
        cls.technique_attribute_value_2 = cls.env.ref(
            "product_fao_fishing.fishing_technique_att_value_harrows"
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
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.fao_technique_attribute.id,
                            "value_ids": [
                                (4, cls.technique_attribute_value_1.id),
                                (4, cls.technique_attribute_value_2.id),
                            ],
                        },
                    ),
                ],
            }
        )
        cls.fishing_tech_arrow = cls.env.ref(
            "product_fao_fishing.fishing_technique_att_value_harrows"
        )

    def test_fishing_areas_from_attribute(self):
        """
        Test helper method to access directly to FAO fishing area product
        """
        self.assertEqual(len(self.product.fao_fishing_area_ids), 2)
        self.assertEqual(len(self.product.fao_fishing_technique_ids), 2)
