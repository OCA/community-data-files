# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # The field unece_due_date_id was present in v13 with ondelete='restrict'
    # and dropped in v14. So we need to set to to null to avoid an error
    # when odoo will try to delete the entries in unece.code.list
    sql = "UPDATE account_tax SET unece_due_date_id=null, unece_due_date_code=null"
    openupgrade.logged_query(env.cr, sql)
