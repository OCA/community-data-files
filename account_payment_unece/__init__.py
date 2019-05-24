# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models

from odoo import api, SUPERUSER_ID


def _assign_account_payment_method_unece_id(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    code_means_31 = env.ref('account_payment_unece.payment_means_31')
    manual_out = env.ref('account.account_payment_method_manual_out')
    manual_in = env.ref('account.account_payment_method_manual_in')
    (manual_out + manual_in).write({
        'unece_id': code_means_31.id,
        'unece_code': code_means_31.code,
    })
