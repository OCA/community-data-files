# Copyright 2024 Moduon
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import requests

from odoo import models

ENDPOINT = "https://publications.europa.eu/webapi/rdf/sparql"
# List of languages imported in previous versions of the module.
ALLOWED_LANGUAGES = [
    "BG",
    "CS",
    "DA",
    "DE",
    "EN",
    "EL",
    "ES",
    "ET",
    "FR",
    "FI",
    "HR",
    "HU",
    "IT",
    "LT",
    "LV",
    "MT",
    "NL",
    "PL",
    "PT",
    "RO",
    "SK",
    "SL",
    "SV",
]


class ResPartnerIndustryEUNaceWizard(models.TransientModel):
    """
    Wizard to import the NACE data from the new ShowVoc endpoint
    https://showvoc.op.europa.eu/ as RAMON is deprecated. The data is stored in
    a SPARQL database in a Resource Description Framework (RDF) format.

    Each element is a resource given in the format of an XML file. The data is
    related semantically by the SKOS thesaurus (https://www.w3.org/TR/skos-reference/)
    and the NACE2 thesaurus (https://data.europa.eu/ux2/nace2/). Also a element
    is identified by a unique URI code, and used as a foreing key in the related
    elements.

    The wizard creates the partner industries from the NACE data and adds the
    parent child relation.
    """

    _name = "res.partner.industry.eu.nace.wizard"
    _description = "Partner Industry by EU NACE Wizard"

    def get_languages(self):
        """Return a list of tuples with the language code and the language name
        in uppercase. If the language is not in the allowed languages list,
        the language code is replaced by "EN". Always adds the "en_US"
        language for the query to work properly."""
        self.ensure_one()
        active_languages = self.env["res.lang"].search([]).mapped("code")
        languages = [(lang, lang.split("_")[0].upper()) for lang in active_languages]
        valid_languages = [
            lang if lang[1] in ALLOWED_LANGUAGES else (lang[0], "EN")
            for lang in languages
        ]
        if ("en_US", "EN") not in valid_languages:
            valid_languages += [("en_US", "EN")]
        return valid_languages

    @staticmethod
    def get_select_query(language):
        return f"?{language}"

    @staticmethod
    def get_skos_query(language):
        return f"skos:altLabel ?Label{language};"

    @staticmethod
    def get_filter_query(language):
        return f"""FILTER (LANG(?Label{language}) = "{language.lower()}")
        BIND (STR(?Label{language}) as ?{language})"""

    def _create_query(self, language_list):
        """Create the query to get the NACE data in the selected languages.
        English is always added for filtering."""
        # ditch duplicates
        languages = list({lang[1] for lang in language_list})
        select_query = " ".join(list(map(self.get_select_query, languages)))
        skos_query = "\n".join(list(map(self.get_skos_query, languages)))
        filter_query = "\n".join(list(map(self.get_filter_query, languages)))
        query = rf"""
            PREFIX : <http://data.europa.eu/ux2/nace2/>
            PREFIX cc: <http://creativecommons.org/ns#>
            PREFIX dc: <http://purl.org/dc/elements/1.1/>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX eli: <http://data.europa.eu/eli/ontology#>
            PREFIX euvoc: <http://publications.europa.eu/ontology/euvoc#>
            PREFIX fn: <http://www.w3.org/2005/xpath-functions#>
            PREFIX gn: <http://www.geonames.org/ontology#>
            PREFIX grddl: <http://www.w3.org/2003/g/data-view#>
            PREFIX iso-thes: <http://purl.org/iso25964/skos-thes#>
            PREFIX luc: <http://www.ontotext.com/owlim/lucene#>
            PREFIX nace21: <http://data.europa.eu/ux2/nace2.1/>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdf4j: <http://rdf4j.org/schema/rdf4j#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX sesame: <http://www.openrdf.org/schema/sesame#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
            PREFIX temporalDescriptions:
            <http://publications.europa.eu/ontology/euvoc/temporalDescriptions#>
            PREFIX vann: <http://purl.org/vocab/vann/>
            PREFIX voaf: <http://purl.org/vocommons/voaf#>
            PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
            PREFIX xkos: <http://rdf-vocabulary.ddialliance.org/xkos#>
            PREFIX xml: <http://www.w3.org/XML/1998/namespace>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT ?LEVEL ?code ?parentCode {select_query} WHERE {{
                ?s skos:inScheme :nace2 ;
                {skos_query}
                skos:notation ?code;
                skos:broader ?parent;
                ^skos:member ?Member.
                ?parent skos:notation ?parentCode .
                {filter_query}
                FILTER (?Member = :sections || ?Member = :divisions  ||
                ?Member = :groups || ?Member = :classes)
                BIND (STR(?Member) AS ?NACELEVEL)
                BIND (STRAFTER(?NACELEVEL, "/nace2/") AS ?LEVEL)
                ?Member skos:prefLabel ?MemberLabel .
                FILTER (LANG(?MemberLabel) = "en")
                BIND (xsd:integer(REPLACE(?code, "\\D", "")) AS ?code_formatted)
                }} ORDER BY ?code_formatted
        """
        return query

    def _create_nace_industry(self, nace_data, languages):
        """Creates the partner industry records from the NACE data and adds it's
        translations."""
        nace_ids = self.env["res.partner.industry"]
        nace_json = nace_data.json()
        bindings = nace_json.get("results", {}).get("bindings", {})
        all_naces = nace_ids.search_read([], ["full_name"])
        nace_map = {
            nace.get("full_name").split(" - ")[0]: nace.get("id") for nace in all_naces
        }
        for binding in bindings:
            nace_code = binding.get("code", {}).get("value", "")
            nace_id = nace_map.get(nace_code, False)
            nace_parent_code = binding.get("parentCode", {}).get("value", "")
            parent_id = nace_map.get(nace_parent_code, False)
            nace_name = binding.get("EN", {}).get("value")
            if not nace_id:
                nace = self.env["res.partner.industry"].create(
                    {
                        "name": nace_name,
                        "full_name": f"{nace_code} - {nace_name}",
                        "parent_id": parent_id,
                    }
                )
                nace_map[nace_code] = nace.id
                nace_ids |= nace
            for lang, lang_code in languages:
                nace_translated = binding.get(lang_code, {}).get("value")
                nace = nace_ids.browse(nace_map[nace_code])
                nace.with_context(lang=lang).write(
                    {
                        "name": nace_translated,
                        "full_name": f"{nace_code} - {nace_translated}",
                    }
                )
        return nace_ids

    def update_partner_industry_eu_nace(self):
        languages = self.get_languages()
        headers = {
            "User-Agent": f"Mozilla/5.0 "
            f"(compatible; Odoo/l10n_eu_nace; "
            f"+{self.get_base_url()})",
        }
        query = self._create_query(languages)
        result = requests.get(
            ENDPOINT,
            params={"format": "json", "query": query},
            headers=headers,
            timeout=120,
        )
        result.raise_for_status()
        nace_ids = self._create_nace_industry(result, languages)
        return nace_ids

    def action_partner_industry_eu_nace(self):
        self.update_partner_industry_eu_nace()
        list_view_id = self.env.ref("base.res_partner_industry_view_tree").id
        return {
            "name": self.env._("Partner Industries by EU NACE"),
            "view_mode": "list",
            "res_model": "res.partner.industry",
            "view_id": list_view_id,
            "type": "ir.actions.act_window",
            "domain": [],
        }
