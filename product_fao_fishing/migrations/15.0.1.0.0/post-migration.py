# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936
from psycopg2 import sql


def _map_fao_technic_values_to_attributes_values(env):
    """Search old product.fao.fishing.technique values for attributes values.
    If the attr has not been found. We create new one
    """
    tech_attribute = env.ref("product_fao_fishing.fao_fishing_technique")
    query = sql.SQL("SELECT id, name FROM {table}").format(
        table=sql.Identifier(
            openupgrade.get_legacy_name("product_fao_fishing_technique")
        )
    )
    env.cr.execute(query)
    results = env.cr.dictfetchall()
    att_values_name = tech_attribute.value_ids.mapped("name")
    values_to_create = {r["name"] for r in results if r["name"] not in att_values_name}
    env["product.attribute.value"].create(
        [{"name": name, "attribute_id": tech_attribute.id} for name in values_to_create]
    )


def _assign_att_value_to_product_template(env):
    """Assign the attribute value to product template based on older
    fao_fishing_technique_id field
    """
    tech_attribute = env.ref("product_fao_fishing.fao_fishing_technique")
    query = sql.SQL(
        """
        select pt.id, pt.name AS product_name, pfft.name AS technic_name
            FROM product_template pt LEFT JOIN {legacy_table} pfft
                ON pt.{legacy_field} = pfft.id
        WHERE pt.{legacy_field} IS NOT NULL
    """
    ).format(
        legacy_table=sql.Identifier(
            openupgrade.get_legacy_name("product_fao_fishing_technique")
        ),
        legacy_field=sql.Identifier(
            openupgrade.get_legacy_name("fao_fishing_technique_id")
        ),
    )
    env.cr.execute(query)
    vals_list = []
    for row in env.cr.dictfetchall():
        attribute_value = tech_attribute.value_ids.filtered(
            lambda atv: atv.name == row["technic_name"]
        )
        if attribute_value:
            vals_list.append(
                {
                    "product_tmpl_id": row["id"],
                    "attribute_id": tech_attribute.id,
                    "value_ids": [(4, attribute_value.id)],
                    "product_template_value_ids": [
                        (
                            0,
                            0,
                            {
                                "product_attribute_value_id": attribute_value.id,
                                "attribute_id": tech_attribute.id,
                            },
                        )
                    ],
                }
            )
    env["product.template.attribute.line"].create(vals_list)


@openupgrade.migrate()
def migrate(env, version):
    _map_fao_technic_values_to_attributes_values(env)
    _assign_att_value_to_product_template(env)
