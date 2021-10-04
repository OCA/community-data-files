# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


def migrate(cr, version):
    if not version:
        return
    # Empty 'account_tax.unece_due_date_id' field as this column will be removed
    # automatically post-migration.
    # This avoids triggering the 'on delete restrict' foreign-key constraint
    # when 'unece.code.list' records of type 'date' are removed from the database.
    query = """
        UPDATE account_tax
        SET unece_due_date_id = NULL
        WHERE unece_due_date_id IS NOT NULL;
    """
    cr.execute(query)
