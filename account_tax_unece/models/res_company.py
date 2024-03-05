# Copyright 2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.tools import html2plaintext, is_html_empty


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_tax_unece_speeddict(self):
        self.ensure_one()
        res = {}
        tax_obj = self.env["account.tax"]
        all_taxes = tax_obj.with_context(active_test=False).search_read(
            [("company_id", "=", self.id)],
            [
                "unece_type_code",
                "unece_categ_code",
                "tax_exigibility",
                "amount",
                "amount_type",
                "name",
                "display_name",
            ],
        )
        for tax in all_taxes:
            res[tax["id"]] = {
                "unece_type_code": tax["unece_type_code"] or None,
                "unece_categ_code": tax["unece_categ_code"] or None,
                "unece_due_date_code": None,
                "amount_type": tax["amount_type"],
                "amount": tax["amount"],
                "name": tax["name"],
                "display_name": tax["display_name"],
            }
            if tax["tax_exigibility"]:
                res[tax["id"]][
                    "unece_due_date_code"
                ] = tax_obj._get_unece_code_from_tax_exigibility(tax["tax_exigibility"])
        return res

    def _get_fiscal_position_speeddict(self, lang):
        self.ensure_one()
        res = {}
        fp_obj = self.env["account.fiscal.position"]
        fpositions = fp_obj.with_context(lang=lang, active_test=False).search_read(
            [("company_id", "=", self.id)], ["name", "display_name", "note"]
        )
        for fp in fpositions:
            note = False
            if fp["note"] and not is_html_empty(fp["note"]):
                note = html2plaintext(fp["note"])
            res[fp["id"]] = {
                "name": fp["name"],
                "display_name": fp["display_name"],
                "note": note,
                # "note" is a fields.Html() that stores the exemption reason
            }
        return res
