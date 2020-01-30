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
