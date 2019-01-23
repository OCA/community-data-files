# Copyright 2019 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    if version:
        with env.cr.savepoint():
            migrate_nace(env)


def migrate_nace(env):
    cr = env.cr
    new_nace_column_name = openupgrade.get_legacy_name("old_nace")
    logger.info(
        "[MOVE res.partner.category] move old naces to temporary field "
        "'%s' in res_partner", new_nace_column_name)
    query = "ALTER TABLE res_partner ADD COLUMN IF NOT EXISTS %s text" % (
        new_nace_column_name)
    cr.execute(query)
    cr.execute("SELECT id FROM res_partner")
    partners = cr.fetchall()
    for x in partners:
        partner = x[0]
        cr.execute(
            "SELECT name FROM res_partner_category WHERE id IN "
            "(SELECT category_id FROM res_partner_res_partner_category_rel "
            "WHERE partner_id = %s)", (partner,))
        categs = cr.fetchall()
        if not categs:
            continue
        old_naces = "\n".join([categ[0] for categ in categs])
        update_query = "UPDATE res_partner SET %s = '%s' WHERE id = %s" % (
            new_nace_column_name, old_naces, partner)
        cr.execute(update_query)
