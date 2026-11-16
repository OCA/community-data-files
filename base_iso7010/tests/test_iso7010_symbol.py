# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from psycopg2 import IntegrityError

from odoo.tests import TransactionCase
from odoo.tools import mute_logger


class TestIso7010Symbol(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Symbol = cls.env["iso7010.symbol"]
        cls.symbol = cls.Symbol.create(
            {
                "name": "Wear eye protection",
                "iso_code": "M004",
                "category": "mandatory",
            }
        )

    def test_display_name(self):
        self.assertEqual(self.symbol.display_name, "[M004] Wear eye protection")

    def test_display_name_recomputed(self):
        self.symbol.name = "Wear safety goggles"
        self.assertEqual(self.symbol.display_name, "[M004] Wear safety goggles")

    def test_name_search_by_name(self):
        self.assertIn(self.symbol, self.Symbol.search([("name", "ilike", "eye")]))

    def test_iso_code_unique(self):
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.Symbol.create(
                {
                    "name": "Duplicate",
                    "iso_code": "M004",
                    "category": "mandatory",
                }
            )
            self.Symbol.flush_model()
