# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, "dangerous_uom"):
        openupgrade.rename_models(env.cr, [("dangerous.uom", "adr.dangerous.uom")])
        openupgrade.rename_tables(env.cr, [("dangerous_uom", "adr_dangerous_uom")])

    if openupgrade.table_exists(env.cr, "limited_amount"):
        openupgrade.rename_models(env.cr, [("limited.amount", "adr.limited.amount")])
        openupgrade.rename_tables(env.cr, [("limited_amount", "adr_limited_amount")])

    if openupgrade.table_exists(env.cr, "packaging_type"):
        openupgrade.rename_models(env.cr, [("packaging.type", "adr.packaging.type")])
        openupgrade.rename_tables(env.cr, [("packaging_type", "adr_packaging_type")])

    if openupgrade.table_exists(env.cr, "storage_class"):
        openupgrade.rename_models(env.cr, [("storage.class", "adr.storage.class")])
        openupgrade.rename_tables(env.cr, [("storage_class", "adr_storage_class")])

    if openupgrade.table_exists(env.cr, "storage_temp"):
        openupgrade.rename_models(env.cr, [("storage.temp", "adr.storage.temp")])
        openupgrade.rename_tables(env.cr, [("storage_temp", "adr_storage_temp")])

    if openupgrade.table_exists(env.cr, "wgk_class"):
        openupgrade.rename_models(env.cr, [("wgk.class", "adr.wgk.class")])
        openupgrade.rename_tables(env.cr, [("wgk_class", "adr_wgk_class")])

    if not openupgrade.column_exists(
        env.cr, "product_product", "adr_limited_amount_id"
    ):
        field_specs = [
            (
                "product.product",
                "product_product",
                "limited_amount_id",
                "adr_limited_amount_id",
            ),
        ]
        openupgrade.rename_fields(env, field_specs)

    if not openupgrade.column_exists(env.cr, "product_product", "adr_dangerous_uom_id"):
        field_specs = [
            (
                "product.product",
                "product_product",
                "dg_unit",
                "adr_dangerous_uom_id",
            ),
        ]
        openupgrade.rename_fields(env, field_specs)

    if not openupgrade.column_exists(env.cr, "product_product", "storage_class_id"):
        field_specs = [
            (
                "product.product",
                "product_product",
                "storage_class_id",
                "adr_storage_class_id",
            ),
        ]
        openupgrade.rename_fields(env, field_specs)

    if not openupgrade.column_exists(env.cr, "product_product", "packaging_type_id"):
        field_specs = [
            (
                "product.product",
                "product_product",
                "packaging_type_id",
                "adr_packaging_type_id",
            ),
        ]
        openupgrade.rename_fields(env, field_specs)

    if not openupgrade.column_exists(env.cr, "product_product", "storage_temp_id"):
        field_specs = [
            (
                "product.product",
                "product_product",
                "storage_temp_id",
                "adr_storage_temp_id",
            ),
        ]
        openupgrade.rename_fields(env, field_specs)

    if not openupgrade.column_exists(env.cr, "product_product", "wgk_class_id"):
        field_specs = [
            (
                "product.product",
                "product_product",
                "wgk_class_id",
                "adr_wgk_class_id",
            ),
        ]
        openupgrade.rename_fields(env, field_specs)
