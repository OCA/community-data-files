# Copyright 2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models


class AccountSetupBankManualConfig(models.TransientModel):
    _inherit = "account.setup.bank.manual.config"

    @api.onchange("acc_number")
    def _onchange_acc_number_base_bank_from_iban(self):
        if not self.acc_number:
            return
        partner_bank = self.env["res.partner.bank"].new({"acc_number": self.acc_number})
        partner_bank._onchange_acc_number_base_bank_from_iban()
        self.update(
            {
                "acc_number": partner_bank.acc_number,
                "bank_id": partner_bank.bank_id.id,
            }
        )
