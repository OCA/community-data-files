# Copyright 2025 ForgeFlow, S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """base.ZWL was removed from base in 18.0 and replaced by base.ZIG.

    The data file is noupdate, so the ISO 4217 values are not written on
    base.ZIG when upgrading. Set them here.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    currency = env.ref("base.ZIG", raise_if_not_found=False)
    if currency:
        currency.with_context(lang="en_US").write(
            {"full_name": "Zimbabwe Gold", "numeric_code": "924"}
        )
