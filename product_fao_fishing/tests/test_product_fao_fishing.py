# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import SavepointCase
from odoo.exceptions import ValidationError


class TestProductFaoFishing(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.template'].create({
            'name': 'test',
        })
        cls.fishing_tech_arrow = cls.env.ref(
            'product_fao_fishing.fishing_technique_harrows')
        cls.my_tech = cls.env['product.fao.fishing.technique'].create({
            'name': 'My Tech',
            'parent_id': cls.fishing_tech_arrow.id
        })

    def test_fishing_technique_name(self):
        self.assertEqual(self.my_tech.complete_name, '{} / {}'.format(
            self.fishing_tech_arrow.name, self.my_tech.name
        ))

    def test_recursion(self):
        with self.assertRaises(ValidationError):
            self.my_tech.parent_id = self.my_tech
