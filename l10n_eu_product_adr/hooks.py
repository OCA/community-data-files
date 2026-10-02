# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tools.sql import table_exists

from .models.common import category_points_factor_map, un_number_points_factor_map


def fill_adr_factor(cr):
    """Creating and populating `product_product.adr_factor`

    Having the ORM calculate the field record by record is unfeasible with an
    extensive product catalog; therefore, the column is added with a default
    value of 0 (an instantaneous operation that does not require rewriting the
    table), and only those products considered dangerous goods are updated, in
    a single pass.
    """
    cr.execute(
        """
        ALTER TABLE product_product
        ADD COLUMN IF NOT EXISTS adr_factor integer DEFAULT 0
        """
    )
    if not table_exists(cr, "adr_goods"):
        return
    # The UN number factor takes precedence over the transport category one
    un_whens = " ".join(["WHEN %s THEN %s"] * len(un_number_points_factor_map))
    category_whens = " ".join(["WHEN %s THEN %s"] * len(category_points_factor_map))
    params = [
        value
        for factor_map in (un_number_points_factor_map, category_points_factor_map)
        for item in factor_map.items()
        for value in item
    ]
    cr.execute(
        f"""
        UPDATE product_product pp
        SET adr_factor = COALESCE(
            CASE ag.un_number {un_whens} END,
            CASE ag.transport_category {category_whens} END,
            0
        )
        FROM adr_goods ag
        WHERE pp.adr_goods_id = ag.id
          AND pp.adr_factor IS DISTINCT FROM COALESCE(
            CASE ag.un_number {un_whens} END,
            CASE ag.transport_category {category_whens} END,
            0
          )
        """,
        params * 2,
    )


def pre_init_hook(env):
    fill_adr_factor(env.cr)
