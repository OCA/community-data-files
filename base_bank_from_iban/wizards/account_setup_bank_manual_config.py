# Copyright 2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models


class AccountSetupBankManualConfig(models.TransientModel):
    _inherit = "account.setup.bank.manual.config"

    @api.onchange("account_number")
    def _onchange_account_number_base_bank_from_iban(self):
        for wizard in self:
            if not wizard.account_number:
                continue
            account = self.env["res.partner.bank"].new(
                {"account_number": wizard.account_number}
            )
            account._onchange_account_number_base_bank_from_iban()
            wizard.update(
                {
                    "account_number": account.account_number,
                    "bank_name": account.bank_name,
                    "bank_bic": account.bank_bic,
                    "country_id": account.country_id.id,
                }
            )
