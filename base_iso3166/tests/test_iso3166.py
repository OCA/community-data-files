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
            return SimpleNamespace(alpha3="AND", numeric="020")

        with patch("pycountry.countries.get", side_effect=fake_get):
            country.write({"code": "AD"})  # dispara recompute
            self.assertEqual(country.code_alpha3, "AND")
            self.assertEqual(country.code_numeric, "020")

    def test_fallback_alpha3_when_alpha_3_not_exist(self):
        """Test que cubre cuando el objeto solo tiene alpha3 (sin alpha_3)"""
        country = self.env.ref("base.ad")

        # Mock que devuelve objeto sin alpha_3, solo alpha3
        def fake_get(**kwargs):
            return SimpleNamespace(alpha3="AND", numeric="020")

        with patch("pycountry.countries.get", side_effect=fake_get):
            country.write({"code": "AD"})
            self.assertEqual(country.code_alpha3, "AND")
            self.assertEqual(country.code_numeric, "020")

    def test_historic_countries_after_countries_fail(self):
        """Test que cubre cuando countries no encuentra y luego historic_countries sí"""
        country = self.env.ref("base.ad")

        # Mock: countries no encuentra, historic_countries sí
        with (
            patch("pycountry.countries.get", return_value=None),
            patch(
                "pycountry.historic_countries.get",
                side_effect=lambda **kw: (
                    SimpleNamespace(alpha3="AND", numeric="020")
                    if (kw.get("alpha_2") == "AD" or kw.get("alpha2") == "AD")
                    else None
                ),
            ),
        ):
            country.write({"code": "AD"})
            self.assertEqual(country.code_alpha3, "AND")
            self.assertEqual(country.code_numeric, "020")

    def test_historic_countries_fallback_alpha2_keyerror(self):
        """Test handling of KeyError in historic_countries loop."""
        country = self.env.ref("base.ad")

        # Mock countries.get -> None (to force loop to historic_countries)
        # Mock historic_countries.get -> KeyError on alpha_2, Success on alpha2
        def historic_get(**kwargs):
            if "alpha_2" in kwargs:
                raise KeyError("alpha_2 not supported")
            return SimpleNamespace(alpha3="AND", numeric="020")

        with (
            patch("pycountry.countries.get", return_value=None),
            patch("pycountry.historic_countries.get", side_effect=historic_get),
        ):
            country.write({"code": "AD"})
            self.assertEqual(country.code_alpha3, "AND")
            self.assertEqual(country.code_numeric, "020")

    def test_countries_keyerror_and_fallback_fail(self):
        """Test path where KeyError is caught but fallback also returns None"""
        country = self.env.ref("base.ad")

        def fake_get(**kwargs):
            if "alpha_2" in kwargs:
                raise KeyError("alpha_2 fail")
            # Fallback alpha2 called, returns None (not found)
            return None

        # We patch both because the loop continues to historic_countries if
        # first one fails/returns None. We want to ensure the final result is
        # False if nothing is found anywhere.
        with (
            patch("pycountry.countries.get", side_effect=fake_get),
            patch("pycountry.historic_countries.get", return_value=None),
        ):
            country.write({"code": "AD"})
            self.assertFalse(country.code_alpha3)
            self.assertFalse(country.code_numeric)
