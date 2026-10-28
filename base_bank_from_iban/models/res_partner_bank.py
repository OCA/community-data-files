# Copyright 2017 Tecnativa - Carlos Dauden
# Copyright 2024 Tecnativa - Pedro M. Baeza
# Copyright 2026 Tecnativa - Adasat Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

import schwifty

from odoo import api, models
from odoo.tools.bank_account_number import format_account_number


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    @api.model_create_multi
    def create(self, vals_list):
        return super().create([self._add_bank_vals(vals) for vals in vals_list])

    def write(self, vals):
        return super().write(self._add_bank_vals(vals))

    @api.model
    def _add_bank_vals(self, vals):
        vals = dict(vals)
        if vals.get("account_number"):
            for field, value in self._get_bank_from_iban(
                vals["account_number"]
            ).items():
                vals.setdefault(field, value)
        return vals

    @api.model
    def _get_bank_from_iban(self, account_number):
        """Return bank details directly usable on an Odoo 20 bank account."""
        try:
            iban = schwifty.IBAN(account_number)
        except schwifty.exceptions.SchwiftyException:
            return {}
        country = self.env["res.country"].search(
            [("code", "=", iban.country_code)], limit=1
        )
        bank = iban.bank or {}
        return {
            "bank_name": bank.get("name") or False,
            "bank_bic": bank.get("bic") or False,
            "country_id": country.id,
        }

    @api.onchange("account_number")
    def _onchange_account_number_base_bank_from_iban(self):
        for account in self:
            if account.account_number:
                vals = account._get_bank_from_iban(account.account_number)
                if vals:
                    vals["account_number"] = format_account_number(
                        self.env, account.account_number
                    ).upper()
                    account.update(vals)
