# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        CREATE TABLE IF NOT EXISTS sanitary_registry
        (
            id serial primary key,
            name varchar
        )
        """,
    )
    # Create sanitary.registry records for values set on company
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO sanitary_registry (name)
        SELECT sanitary_registry
        FROM res_company
        WHERE sanitary_registry IS NOT NULL
            AND NOT EXISTS (
              SELECT 1 FROM sanitary_registry LIMIT 1
            )
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE res_company
            ADD COLUMN IF NOT EXISTS sanitary_registry_id integer
        """,
    )
    # Assign the sanitary.registry record to res.company
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_company rc
        SET sanitary_registry_id = sr.id FROM sanitary_registry sr
        WHERE sr.name = rc.sanitary_registry
        """,
    )
