# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.addons.l10n_eu_product_adr.hooks import (  # pylint: disable=odoo-addons-relative-import
    fill_adr_factor,
)


def migrate(cr, version):
    if not version:
        return
    fill_adr_factor(cr)
