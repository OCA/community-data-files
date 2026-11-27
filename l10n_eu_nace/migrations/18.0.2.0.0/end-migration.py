# Copyright 2026 Moduon Team S.L. <info@moduon.team>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# It's an end script so that all the modules are loaded, e.g. crm_industry,
# whose leads must be moved too.
from odoo import SUPERUSER_ID, api

from odoo.addons.l10n_eu_nace.hooks import migrate_to_nace21


def migrate(cr, version):
    migrate_to_nace21(api.Environment(cr, SUPERUSER_ID, {}))
