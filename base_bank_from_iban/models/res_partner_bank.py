# Copyright 2017 Tecnativa - Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3).

from odoo import api, models

from odoo.addons.base_iban.models.res_partner_bank import (
    _map_iban_template,
    normalize_iban,
    pretty_iban,
)


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    @api.onchange("acc_number", "acc_type")
    def _onchange_acc_number_base_bank_from_iban(self):
        if self.acc_type != "iban":
            return
        acc_number = pretty_iban(normalize_iban(self.acc_number)).upper()
        country_code = self.acc_number[:2].lower()
        iban_template = _map_iban_template[country_code]
        first_match = iban_template[2:].find("B") + 2
        last_match = iban_template.rfind("B") + 1
        bank_code = acc_number[first_match:last_match].replace(" ", "")
        bank = self.env["res.bank"].search(
            [("code", "=", bank_code), ("country.code", "=", country_code.upper())],
            limit=1,
        )
        self.update({"bank_id": bank.id, "acc_number": acc_number})
