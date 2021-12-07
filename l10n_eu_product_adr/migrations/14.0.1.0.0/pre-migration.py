# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

_logger = logging.getLogger(__name__)

try:
    from openupgradelib import openupgrade
except (ImportError, IOError) as err:
    _logger.debug(err)


PREVIOUS_MODULE_NAME = "l10n_eu_product_adr"
NEW_MODULE_NAME = "l10n_eu_product_adr_dangerous_good"


QUERY_GET_NAMES = """
    SELECT name
    FROM ir_model_data
    WHERE module = %s
    AND model in %s;
"""

FIELD_NAMES_TO_MOVE = {
    "product.product": [
        "limited_amount_id",
        "content_package",
        "nag",
        "veva_code_empty",
        "veva_code_full",
        "storage_class_id",
        "packaging_type_id",
        "storage_temp_id",
        "flash_point",
        "wgk_class_id",
        "h_no",
        "envir_hazardous ",
        "packaging_group ",
        "hazard_ind ",
        "voc ",
        "content_package ",
        "label_first ",
        "label_second ",
        "label_third ",
        "dg_unit",
    ],
}
MODELS_TO_MOVE = (
    "storage.class",
    "packaging.type",
    "storage.temp",
    "wgk.class",
    "limited.amount",
    "dangerous.uom",
)


def move_fields_to_new_module(cr):
    for model, field_names in FIELD_NAMES_TO_MOVE.items():
        openupgrade.update_module_moved_fields(
            cr, model, field_names, PREVIOUS_MODULE_NAME, NEW_MODULE_NAME
        )


def move_records_to_new_module(cr):
    cr.execute(QUERY_GET_NAMES, (PREVIOUS_MODULE_NAME, MODELS_TO_MOVE))
    # Result is [(None, )] if empty [([names])] otherwise
    xmlid_names = [row[0] for row in cr.fetchall()]
    if not xmlid_names:
        return
    xmlids = [
        (f"{PREVIOUS_MODULE_NAME}.{name}", f"{NEW_MODULE_NAME}.{name}")
        for name in xmlid_names
    ]
    openupgrade.rename_xmlids(cr, xmlids)


def backup_adr_code(cr):
    # Create a new column in which we store the related adr code,
    # so that we will be able to retrieve the adr.goods record in the
    # post migration script.
    cr.execute("ALTER TABLE product_product ADD adr_number varchar;")
    backup_query = """
        UPDATE product_product pp
        SET adr_number = ur.name
        FROM un_reference ur
        WHERE ur.id = pp.un_ref
        AND pp.un_ref IS NOT NULL;
    """
    cr.execute(backup_query)


def update_transport_category(cr):
    # In the previous version (13.0) the transport category selection was
    # [("1", "0"), ("2", "1"), ("3", "2"), ("4", "3"), ("5", "4")]
    # In the new one, the selection has been updated like so
    # [
    #     ("0", "0"),
    #     ("1", "1"),
    #     ("2", "2"),
    #     ("3", "3"),
    #     ("4", "4"),
    #     ("-", "-"),
    #     ("CARRIAGE_PROHIBITED", "CARRIAGE PROHIBITED"),
    #     ("NOT_SUBJECT_TO_ADR", "Not subject to ADR"),
    # ]
    # Updating this now, so we can find the right adr.goods record
    # in the post script
    for prev, new in enumerate(range(5), start=1):
        query = """
            UPDATE product_product
            SET transport_category = %(new)s
            WHERE transport_category = %(prev)s;
        """
        cr.execute(query, {"new": str(new), "prev": str(prev)})


def migrate(cr, version):
    update_transport_category(cr)
    # Move fields and records not present in the new implementation to
    # `l10n_eu_product_adr_dangerous_good`.
    move_fields_to_new_module(cr)
    move_records_to_new_module(cr)
    # Backup the adr code on product
    backup_adr_code(cr)
