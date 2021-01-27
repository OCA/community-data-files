# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        for template in env["product.template"].search([]):
            for variant in template.product_variant_ids:
                variant.sds = template.sds
                variant.content_package = template.content_package

    cr.execute("ALTER TABLE product_template DROP COLUMN sds;")
    cr.execute("ALTER TABLE product_template DROP COLUMN content_package;")
