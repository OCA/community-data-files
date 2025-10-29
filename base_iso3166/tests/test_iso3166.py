# Copyright 2017 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from types import SimpleNamespace
from unittest.mock import patch

from odoo.tests import common


class TestBaseIso3166(common.TransactionCase):
    def test_iso_3166(self):
        country = self.env.ref("base.ad")
        self.assertEqual(country.code_alpha3, "AND")
        self.assertEqual(country.code_numeric, "020")

    def test_historic_countries(self):
        ussr = self.env["res.country"].create(
            {"code": "SU", "name": "USSR, Union of Soviet Socialist Republics"}
        )
        self.assertEqual(ussr.code_alpha3, "SUN")
        self.assertEqual(ussr.code_numeric, "810")

    def test_recompute_on_code_change(self):
        country = self.env.ref("base.ad")
        self.assertEqual(country.code_alpha3, "AND")
        self.assertEqual(country.code_numeric, "020")

        country.write({"code": "ZZ"})  # no existe en ISO
        self.assertFalse(country.code_alpha3)
        self.assertFalse(country.code_numeric)

        country.write({"code": "AD"})  # restaurar
        self.assertEqual(country.code_alpha3, "AND")
        self.assertEqual(country.code_numeric, "020")

    def test_fallback_alpha2_when_alpha_2_keyerror(self):
        country = self.env.ref("base.ad")

        def fake_get(**kwargs):
            if "alpha_2" in kwargs:
                raise KeyError("alpha_2 not supported")
            if kwargs.get("alpha2") == "AD":
                return SimpleNamespace(
                    alpha3="AND", numeric="020"
                )  # fuerza fallback alpha3
            return None

        with patch("pycountry.countries.get", side_effect=fake_get):
            country.write({"code": "AD"})  # dispara recompute
            self.assertEqual(country.code_alpha3, "AND")
            self.assertEqual(country.code_numeric, "020")
