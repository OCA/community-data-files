# Copyright 2017 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.onchange("bank_acc_number")
    def _onchange_bank_acc_number_base_bank_from_iban(self):
        if not self.bank_acc_number:
            return
        partner_bank = self.env["res.partner.bank"].new(
            {"acc_number": self.bank_acc_number}
        )
        partner_bank._onchange_acc_number_base_bank_from_iban()
        self.update(
            {
                "bank_acc_number": partner_bank.acc_number,
                "bank_id": partner_bank.bank_id.id,
            }
        )
