# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
try:
    from openupgradelib import openupgrade
except ImportError:
    openupgrade = None


def migrate(cr, version):
    """Move adr data from product_template to product_product"""
    if (
        not openupgrade
        or not openupgrade.column_exists(cr, "product_template", "adr_goods_id")
        or openupgrade.column_exists(cr, "product_product", "adr_goods_id")
    ):
        return
    cr.execute(
        """
        ALTER TABLE product_product
        ADD COLUMN adr_goods_id INTEGER,
        ADD COLUMN is_dangerous BOOLEAN;
        UPDATE product_product pp
        SET adr_goods_id = pt.adr_goods_id,
            is_dangerous = pt.is_dangerous
        FROM product_template pt
        WHERE pt.id = pp.product_tmpl_id
        """
    )
