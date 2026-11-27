# Copyright 2026 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from unittest.mock import patch

import requests

from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.l10n_eu_nace.hooks import (
    NACE2_NACE21,
    migrate_to_nace21,
    read_nace21,
)

WIZARD_MODULE = "odoo.addons.l10n_eu_nace.wizard.res_partner_industry_eu_nace_wizard"


class TestNace2Migration(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.industry = cls.env["res.partner.industry"].with_context(active_test=False)
        # The installation already migrated Odoo's base sections
        cls.nace = cls.industry._get_nace_map()

        # More NACE Rev. 2 industries, as the previous version of the module
        # imported them
        def old(code, name):
            return cls.industry.create({"name": name, "full_name": f"{code} - {name}"})

        cls.stalls = old("47.81", "Retail sale via stalls and markets of food")
        cls.programming = old("62.01", "Computer programming activities")
        cls.consultancy = old("62.02", "Computer consultancy activities")
        # Not NACE Rev. 2, e.g. from a national classification
        cls.hydro = old("35.15", "Production of hydro-electric electricity")
        # Not NACE, created by a user under a NACE Rev. 2 industry
        cls.apps = cls.industry.create(
            {"name": "Mobile apps", "parent_id": cls.programming.id}
        )
        partner = cls.env["res.partner"]
        cls.market = partner.create({"name": "Market", "industry_id": cls.stalls.id})
        cls.software = partner.create(
            {
                "name": "Software",
                "industry_id": cls.programming.id,
                "secondary_industry_ids": [(6, 0, [cls.consultancy.id, cls.stalls.id])],
            }
        )
        cls.dam = partner.create({"name": "Dam", "industry_id": cls.hydro.id})

    def _get(self, code):
        return self.industry.browse(self.nace[code])

    def test_data(self):
        rows = read_nace21()
        self.assertEqual(len(rows), 1047)
        codes = set()
        for row in rows:
            # Parents first
            self.assertTrue(not row["parent_code"] or row["parent_code"] in codes)
            self.assertIn(row["nace2_code"], ("", row["code"]))
            self.assertNotIn(row["nace2_code"], NACE2_NACE21)
            codes.add(row["code"])
        self.assertLessEqual(set(NACE2_NACE21.values()), codes)

    def test_correspondence(self):
        self.assertEqual(len(NACE2_NACE21), 171)
        self.assertEqual(NACE2_NACE21["47.81"], "47.11")
        self.assertEqual(NACE2_NACE21["62.01"], "62.10")
        for source, target in NACE2_NACE21.items():
            self.assertNotEqual(source, target)
            self.assertEqual(len(source), len(target), source)

    def test_install(self):
        """Installing the module migrates Odoo's base sections."""
        self.assertEqual(len(self.nace), 1047)
        base_k = self.env.ref("base.res_partner_industry_K")
        self.assertFalse(base_k.active)
        self.assertEqual(self._get("L").name, "FINANCIAL AND INSURANCE ACTIVITIES")
        # Section A keeps its activity: same record
        self.assertEqual(self._get("A"), self.env.ref("base.res_partner_industry_A"))
        self.assertEqual(self._get("47.81").parent_id, self._get("47.8"))

    def test_migration(self):
        migrate_to_nace21(self.env)
        self.assertEqual(self.industry._get_nace_map(), self.nace)
        # Code with another activity: archived and moved
        self.assertFalse(self.stalls.active)
        self.assertEqual(self.market.industry_id, self._get("47.11"))
        self.assertEqual(self._get("47.81").name, "Retail sale of motor vehicles")
        # Main and secondary industries are moved, without duplicates
        self.assertEqual(self.software.industry_id, self._get("62.10"))
        self.assertEqual(
            self.software.secondary_industry_ids,
            self._get("62.20") | self._get("47.11"),
        )
        # Industries out of NACE Rev. 2 are left alone
        self.assertTrue(self.hydro.active)
        self.assertEqual(self.dam.industry_id, self.hydro)
        # unless they hang from a replaced one
        self.assertTrue(self.apps.active)
        self.assertEqual(self.apps.parent_id, self._get("62.10"))

    def test_search_by_code(self):
        migrate_to_nace21(self.env)
        self.assertEqual(
            self.industry.search([("nace_code_index", "ilike", " nace21:62.1 ")]),
            self._get("62.1"),
        )
        self.assertEqual(
            self.industry.search([("nace_code_index", "ilike", " nace2:62.01 ")]),
            self.programming,
        )

    def test_main_industry_not_duplicated_in_secondary(self):
        self.software.write(
            {
                "industry_id": self.stalls.id,
                "secondary_industry_ids": [(6, 0, self._get("47.11").ids)],
            }
        )
        migrate_to_nace21(self.env)
        self.assertEqual(self.software.industry_id, self._get("47.11"))
        self.assertFalse(self.software.secondary_industry_ids)

    def test_rerun(self):
        migrate_to_nace21(self.env)
        before = self.industry.search([]).read(["name", "active", "parent_id"])
        migrate_to_nace21(self.env)
        self.assertEqual(
            self.industry.search([]).read(["name", "active", "parent_id"]), before
        )

    def test_wizard_no_connection(self):
        wizard = self.env["res.partner.industry.eu.nace.wizard"].create({})
        with (
            patch(
                f"{WIZARD_MODULE}.requests.get",
                side_effect=requests.ConnectionError("offline"),
            ),
            self.assertRaises(UserError),
        ):
            wizard.action_partner_industry_eu_nace()
