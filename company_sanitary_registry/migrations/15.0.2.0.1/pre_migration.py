# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        CREATE TABLE IF NOT EXISTS sanitary_registry_warehouse_category
        (
            id serial primary key,
            sanitary_registry_id integer,
            categoy_id integer,
            warehouse_id integer,
        )
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO sanitary_registry_warehouse_category (sanitary_registry_id, category_id)
        SELECT sanitary_registry_id, id as category_id
        FROM product_category
        WHERE sanitary_registry_id IS NOT NULL;
        """,
    )
