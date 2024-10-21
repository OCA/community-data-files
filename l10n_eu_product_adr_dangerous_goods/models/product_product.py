# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models

LABELS_SELECTION = [
    ("1", "2"),
    ("2", "2.1"),
    ("3", "2.2"),
    ("4", "3"),
    ("5", "4.1"),
    ("6", "4.2"),
    ("7", "4.3"),
    ("8", "5.1"),
    ("9", "5.2"),
    ("10", "8"),
    ("11", "9"),
    ("12", "9A"),
]


class ProductProduct(models.Model):
    _inherit = "product.product"

    # To be set manually for the moment. Could eventually be computed after,
    # depending on the dangerous class and the product's weight/captain'sage…
    limited_amount_id = fields.Many2one("limited.amount")

    # package-related fields
    content_package = fields.Float(string="Content Packaging", digits=(16, 5))
    dg_unit = fields.Many2one("dangerous.uom")
    nag = fields.Char(string="N.A.G.")
    veva_code_empty = fields.Char(string="VeVA Code: Empty packaging")
    veva_code_full = fields.Char(string="VeVA Code: Full package")

    # storage-related fields
    storage_class_id = fields.Many2one("storage.class")
    packaging_type_id = fields.Many2one("packaging.type")
    storage_temp_id = fields.Many2one("storage.temp")
    flash_point = fields.Char(string="Flash point(°C)")
    wgk_class_id = fields.Many2one("wgk.class")
    h_no = fields.Char(string="H-No")  # Ho, NoooOOooooO!

    envir_hazardous = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Environmentally hazardous"
    )
    packaging_group = fields.Selection(
        [("1", "(-)"), ("2", "I"), ("3", "II"), ("4", "III")]
    )
    hazard_ind = fields.Char(string="Hazard identification")
    voc = fields.Char(string="VOC in%")
    label_first = fields.Selection(LABELS_SELECTION, string="Label 1")
    label_second = fields.Selection(LABELS_SELECTION, string="Label 2")
    label_third = fields.Selection(LABELS_SELECTION, string="Label 3")
