# Copyright 2024 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from unittest.mock import patch

from odoo.tests import Form
from odoo.tests.common import TransactionCase, new_test_user

from .test_en_nace_request_results import (
    NACE_COMMON,
    NACE_EN,
    NACE_ES,
    NACE_FR,
    create_response,
)

MOCK_PATH = (
    "odoo.addons.l10n_eu_nace.wizard.res_partner_industry_eu_nace_wizard.requests.get"
)


class TestResPartnerIndustryEUNaceWizard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uid = new_test_user(
            cls.env,
            login="test-manager",
            groups="base.group_system",
        )

    def activate_langs(self, lang_list):
        lang_ids = self.env["res.lang"]
        lang_ids.search([("code", "not in", ["en_US"])]).write({"active": False})
        for lang in lang_list:
            lang_ids |= self.env.ref(lang)
        lang_ids.write({"active": True})

    def wizard_eu_nace(self):
        wizard = Form(
            self.env["res.partner.industry.eu.nace.wizard"].with_user(self.uid)
        )
        import_wizard = wizard.save()
        return import_wizard

    def test_get_languages(self):
        nace_wizard = self.wizard_eu_nace()
        self.assertEqual(nace_wizard.get_languages(), [("en_US", "EN")])

        active_languages = ["base.lang_en", "base.lang_es", "base.lang_fr"]
        self.activate_langs(active_languages)
        expected = [("en_US", "EN"), ("es_ES", "ES"), ("fr_FR", "FR")]
        self.assertCountEqual(nace_wizard.get_languages(), expected)

        # test if english is added when no english language is active
        active_languages = ["base.lang_es", "base.lang_fr"]
        self.activate_langs(active_languages)
        self.assertCountEqual(nace_wizard.get_languages(), expected)

        # test for multiple translations of the same language
        active_languages = ["base.lang_es", "base.lang_es_MX", "base.lang_fr"]
        self.activate_langs(active_languages)
        expected = [("en_US", "EN"), ("es_ES", "ES"), ("es_MX", "ES"), ("fr_FR", "FR")]
        self.assertCountEqual(nace_wizard.get_languages(), expected)

        # test when a language has no transaltion in NACE has english as default
        active_languages = ["base.lang_es", "base.lang_my"]
        self.activate_langs(active_languages)
        expected = [("en_US", "EN"), ("es_ES", "ES"), ("my_MM", "EN")]
        self.assertCountEqual(nace_wizard.get_languages(), expected)

    def test_create_query(self):
        nace_wizard = self.wizard_eu_nace()
        active_languages = ["base.lang_en", "base.lang_es", "base.lang_fr"]
        self.activate_langs(active_languages)
        languages = nace_wizard.get_languages()
        query = nace_wizard._create_query(languages)
        self.assertIn("?EN", query)
        self.assertIn("?ES", query)
        self.assertIn("?FR", query)
        self.assertIn("?FR", query)
        self.assertIn("skos:altLabel ?LabelES;", query)
        self.assertIn("skos:altLabel ?LabelEN;", query)
        self.assertIn("skos:altLabel ?LabelFR;", query)
        self.assertIn('FILTER (LANG(?LabelES) = "es")', query)
        self.assertIn("BIND (STR(?LabelES) as ?ES)", query)
        self.assertIn('FILTER (LANG(?LabelEN) = "en")', query)
        self.assertIn("BIND (STR(?LabelEN) as ?EN)", query)
        self.assertIn('FILTER (LANG(?LabelFR) = "fr")', query)
        self.assertIn("BIND (STR(?LabelFR) as ?FR)", query)

    @patch(MOCK_PATH, return_value=create_response(NACE_COMMON, NACE_EN))
    def test_update_partner_industry_eu_nace_english_only(self, mock_request):
        self.activate_langs(["base.lang_en"])
        nace_wizard = self.wizard_eu_nace()
        records_created = nace_wizard.update_partner_industry_eu_nace()
        self.assertEqual(len(records_created), 4)

    @patch(
        MOCK_PATH, return_value=create_response(NACE_COMMON, NACE_EN, NACE_ES, NACE_FR)
    )
    def test_update_partner_industry_eu_nace_multiple_languages_with_english(
        self, mock_request
    ):
        lang_list = ["base.lang_en", "base.lang_es", "base.lang_fr"]
        self.activate_langs(lang_list)
        nace_wizard = self.wizard_eu_nace()
        records_created = nace_wizard.update_partner_industry_eu_nace()
        self.assertEqual(len(records_created), 4)

    @patch(
        MOCK_PATH, return_value=create_response(NACE_COMMON, NACE_EN, NACE_ES, NACE_FR)
    )
    def test_update_partner_industry_eu_nace_no_english(self, mock_request):
        self.activate_langs(["base.lang_es", "base.lang_fr"])
        nace_wizard = self.wizard_eu_nace()
        records_created = nace_wizard.update_partner_industry_eu_nace()
        self.assertEqual(len(records_created), 4)

    @patch(MOCK_PATH, return_value=create_response(NACE_COMMON, NACE_EN, NACE_ES))
    def test_update_partner_industry_eu_nace_new_language_update(self, mock_request):
        self.activate_langs(["base.lang_en", "base.lang_es"])
        nace_wizard = self.wizard_eu_nace()
        records_created = nace_wizard.update_partner_industry_eu_nace()
        self.activate_langs(["base.lang_en", "base.lang_es", "base.lang_fr"])
        mock_request.return_value = create_response(
            NACE_COMMON, NACE_EN, NACE_ES, NACE_FR
        )
        nace_wizard = self.wizard_eu_nace()
        records_translated = nace_wizard.update_partner_industry_eu_nace()
        self.assertEqual(len(records_translated), 0)
        records_created_name_fr = records_created.with_context(lang="fr_FR").mapped(
            "name"
        )
        nace_fr_names = list(map(lambda item: item.get("FR").get("value"), NACE_FR))
        self.assertCountEqual(records_created_name_fr, nace_fr_names)

    @patch(MOCK_PATH, return_value=create_response(NACE_COMMON, NACE_EN, NACE_ES))
    def test_update_partner_industry_eu_nace_idempotent_update(self, mock_request):
        self.activate_langs(["base.lang_en"])
        nace_wizard = self.wizard_eu_nace()
        records_created = nace_wizard.update_partner_industry_eu_nace()
        self.assertEqual(len(records_created), 4)
        nace_wizard = self.wizard_eu_nace()
        records_created = nace_wizard.update_partner_industry_eu_nace()
        self.assertEqual(len(records_created), 0)
