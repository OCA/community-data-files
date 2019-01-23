# Copyright 2019 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import re
import odoo
from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    if version:
        actions = [import_nace, fix_nace_id]
        for action in actions:
            with odoo.api.Environment.manage():
                with odoo.registry(env.cr.dbname).cursor() as new_cr:
                    new_env = odoo.api.Environment(
                        new_cr, env.uid, env.context)
                    action(new_env)


def import_nace(env):
    logger.info(
        "[IMPORT res.partner.nace] download from ramon european service")
    wiz_model = env['nace.import']
    wiz = wiz_model.create({})
    wiz.run_import()


def fix_nace_id(env):
    new_nace_column_name = openupgrade.get_legacy_name("old_nace")
    logger.info(
        "[UDPATE res.partner] reimport old naces from 'res_partner.%s' to "
        "'res_partner_nace'", new_nace_column_name)
    query = "SELECT id, %s FROM res_partner WHERE %s IS NOT NULL" % (
        new_nace_column_name, new_nace_column_name)
    env.cr.execute(query)
    partners = env.cr.fetchall()
    for id_, old_naces in partners:
        nace_codes = []
        for category in old_naces.split('\n'):
            nace_code_match = re.match(r"^\[.*\]", category)
            if nace_code_match:
                nace_codes.append(nace_code_match.group(0).strip("[]"))
        if nace_codes:
            naces = env['res.partner.nace'].search([
                ('code', 'in', nace_codes)])
            partner = env['res.partner'].with_context(
                active_test=False).browse(id_)
            if len(naces) == 1:
                partner.primary_nace_id = naces.id
            elif naces:
                partner.primary_nace_id = naces[0].id
                secondary_naces = naces - naces[0]
                partner.secondary_nace_ids = [(6, 0, secondary_naces.ids)]
