# Copyright 2026 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.base.tests.common import BaseCommon


class TestDisplayName(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.industry = cls.env["res.partner.industry"]
        nace = cls.industry._get_nace_map()
        cls.cereals = cls.industry.browse(nace["01.11"])
        cls.custom = cls.industry.create({"name": "Custom industry"})
        cls.custom_child = cls.industry.create(
            {"name": "Custom child", "parent_id": cls.custom.id}
        )

    def _search(self, value, operator="ilike", lang="en_US"):
        industry = self.industry.with_context(lang=lang)
        return self.industry.browse(
            [i for i, _name in industry.name_search(value, operator=operator)]
        )

    def test_display_name(self):
        """NACE industries show their code and name, without their parents."""
        self.assertEqual(
            self.cereals.display_name,
            "01.11 - Growing of cereals, other than rice, leguminous crops and "
            "oil seeds",
        )
        # Industries out of NACE keep showing the path of their parents
        self.assertEqual(
            self.custom_child.display_name, "Custom industry / Custom child"
        )

    def test_display_name_translated(self):
        self.env["res.lang"]._activate_lang("es_ES")
        self.cereals.with_context(
            lang="es_ES"
        ).full_name = "01.11 - Cultivo de cereales"
        self.assertEqual(
            self.cereals.with_context(lang="es_ES").display_name,
            "01.11 - Cultivo de cereales",
        )
        self.assertIn(self.cereals, self._search("cereales", lang="es_ES"))
        self.assertNotIn(self.cereals, self._search("cereales"))

    def test_search(self):
        """NACE industries are found by code or by name."""
        self.assertIn(self.cereals, self._search("01.11"))
        self.assertIn(self.cereals, self._search("Growing of cereals"))
        self.assertIn(self.cereals, self._search(self.cereals.full_name, "="))
        self.assertNotIn(self.cereals, self._search("01.11", "not ilike"))
        self.assertEqual(self._search("Custom child"), self.custom_child)
