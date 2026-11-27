# Copyright 2026 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.osv import expression


class ResPartnerIndustry(models.Model):
    _inherit = "res.partner.industry"

    nace_codes = fields.Json(
        string="NACE Codes",
        readonly=True,
        copy=False,
        help="Code of the industry in each classification it belongs to, "
        'e.g. {"nace2": "01.11", "nace21": "01.11"}.',
    )
    nace_code_index = fields.Char(
        string="NACE Codes Index",
        compute="_compute_nace_code_index",
        store=True,
        index="trigram",
        help="NACE codes as searchable text, e.g. ' nace2:01.11 nace21:01.11 '. "
        "Search one code with [('nace_code_index', 'ilike', ' nace21:62.10 ')].",
    )

    @api.depends("nace_codes")
    def _compute_nace_code_index(self):
        for industry in self:
            codes = industry.nace_codes or {}
            # Surrounded by spaces, so that searching " nace21:62.1 " doesn't
            # match 62.10
            industry.nace_code_index = (
                " " + " ".join(f"{key}:{codes[key]}" for key in sorted(codes)) + " "
                if codes
                else False
            )

    @api.depends("full_name", "nace_codes")
    def _compute_display_name(self):
        # Industries of a classification show their code and name, e.g.
        # "01.11 - Growing of cereals...", instead of the path of their parents
        res = super()._compute_display_name()
        for industry in self:
            if industry.nace_codes and industry.full_name:
                industry.display_name = industry.full_name
        return res

    def _search_display_name(self, operator, value):
        domain = super()._search_display_name(operator, value)
        if not value:
            return domain
        # Also by code: match the name or the full name, or exclude both
        aggregator = (
            expression.AND
            if operator in expression.NEGATIVE_TERM_OPERATORS
            else expression.OR
        )
        return aggregator([domain, [("full_name", operator, value)]])

    @api.model
    def _get_nace_map(self, classification="nace21"):
        """Return ``{code: industry id}`` for the industries of a classification,
        archived ones included."""
        industries = (
            self.sudo()
            .with_context(active_test=False)
            .search([("nace_code_index", "ilike", f" {classification}:")])
        )
        return {
            industry.nace_codes[classification]: industry.id
            for industry in industries
            if classification in industry.nace_codes
        }
