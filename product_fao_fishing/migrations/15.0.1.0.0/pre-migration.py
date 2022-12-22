# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

_column_renames = {
    "product_template": [
        ("fao_fishing_technique_id", None),
    ],
}
_table_renames = [
    ("product_fao_fishing_technique", None),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(env.cr, _column_renames)
    openupgrade.rename_tables(env.cr, _table_renames)
