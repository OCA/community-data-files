# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestProductMeatUnece(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductMeatUnece, cls).setUpClass()

        # MODELS
        cls.unece_code_list_model = cls.env["unece.code.list"]

    def test_01(self):
        """
        Data:
            - /
        Test case:
            - Try to create a meat code list with a code too long
        Expected result:
            - ValidationError is raised
        """
        with self.assertRaises(ValidationError):
            self.unece_code_list_model.create(
                {"name": "Too long", "type": "meat_species", "code": "123"}
            )

    def test_02(self):
        """
        Data:
            - /
        Test case:
            - Try to create a meat code list with a code too short
        Expected result:
            - ValidationError is raised
        """
        with self.assertRaises(ValidationError):
            self.unece_code_list_model.create(
                {"name": "Too short", "type": "meat_species", "code": "1"}
            )

    def test_03(self):
        """
        Data:
            - /
        Test case:
            - Try to create a meat code list with a valid code
        Expected result:
            - Code list created
        """
        self.assertTrue(
            self.unece_code_list_model.create(
                {"name": "OK", "type": "meat_species", "code": "88"}
            )
        )

    def test_04(self):

        prod = self.env["product.product"].create(
            {
                "name": "test_product",
                "unece_meat_species_id": self.env.ref(
                    "product_meat_unece.unece_meat_species_bovine_beef"
                ).id,
                "unece_meat_product_cut_id": self.env.ref(
                    "product_meat_unece.unece_meat_product_cut_brisket_point_end_1"
                ).id,
                "unece_meat_refrigeration_id": self.env.ref(
                    "product_meat_unece.unece_meat_refrigeration_chilled"
                ).id,
                "unece_meat_bovine_category_id": self.env.ref(
                    "product_meat_unece.unece_meat_bovine_category_intact_male"
                ).id,
            }
        )

        res = prod.unece_meat_code
        self.assertEqual("1016500011000000000", res)
        prod.write(
            {
                "unece_meat_product_cut_id": self.env.ref(
                    "product_meat_unece.unece_meat_product_cut_brisket_rib_plate"
                ).id
            }
        )
        res = prod.unece_meat_code
        self.assertEqual("1017300011000000000", res)
