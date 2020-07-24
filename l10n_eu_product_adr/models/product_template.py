# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models

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

TRANSPORT_CATEGORY = [("1", "0"), ("2", "1"), ("3", "2"), ("4", "3"), ("5", "4")]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_dangerous = fields.Boolean(string="Dangerous product")
    dangerous_class_id = fields.Many2one(
        "product.dangerous.class", string="Dangerous class"
    )
    un_ref = fields.Many2one("un.reference", string="UN Number")
    envir_hazardous = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Environmentally hazardous"
    )
    adr_amount = fields.Char(string="LQ - ADR amount")
    voc = fields.Char(string="VOC in%")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
    )
    veg = fields.Monetary(string="VEG in currency")
    nag = fields.Char(string="N.A.G.")
    veva_code_empty = fields.Char(string="VeVA Code: Empty packaging")
    veva_code_full = fields.Char(string="VeVA Code: Full package")
    un_report = fields.Char(string="UN Report 38.3")
    sds = fields.Char(string="SDS")
    content_package = fields.Float(string="Content Packaging")
    flash_point = fields.Char(string="Flash point(°C)")
    h_no = fields.Char(string="H-No")
    hazard_ind = fields.Char(string="Hazard identification")
    dg_unit = fields.Many2one("dangerous.uom", string="DG - Unit")
    packaging_group = fields.Selection(
        [("1", "(-)"), ("2", "I"), ("3", "II"), ("4", "III")], string="Packaging Group"
    )
    transport_category = fields.Selection(
        TRANSPORT_CATEGORY, string="Transport Category",
    )
    tunnel_code = fields.Selection(
        [("1", "(-)"), ("2", "(D)"), ("3", "(E)"), ("4", "(D,E)")], string="Tunnel code"
    )
    label_first = fields.Selection(LABELS_SELECTION, string="Label 1")
    label_second = fields.Selection(LABELS_SELECTION, string="Label 2")
    label_third = fields.Selection(LABELS_SELECTION, string="Label 3")

    class_id = fields.Many2one("great.class")
    limited_amount_id = fields.Many2one("limited.amount")
    storage_class_id = fields.Many2one("storage.class")
    packaging_type_id = fields.Many2one("packaging.type")
    storage_temp_id = fields.Many2one("storage.temp")
    dangerous_selection_id = fields.Many2one("dangerous.goods")
    wgk_class_id = fields.Many2one("wgk.class")

    is_dangerous_good = fields.Boolean(help="This product belongs to a dangerous class")
    is_dangerous_waste = fields.Boolean(
        help="Waste from this product belongs to a dangerous class"
    )

    @api.onchange("is_dangerous")
    def _ochange_is_dangerous(self):
        self.is_dangerous_good = self.is_dangerous

    def get_full_class_name(self):
        class_name = _("UN")

        if self.is_dangerous_waste:
            class_name += _(" WASTE")
        class_name += " {}, {}".format(self.un_ref.name, self.un_ref.description)

        if self.nag:
            class_name += _(", N.A.G ({})").format(self.nag)

        if self.label_first:
            class_name += ", {}".format(self._get_name_from_selection("label_first"))
        if self.label_second and self.label_third:
            class_name += ", ({}, {})".format(
                self._get_name_from_selection("label_second"),
                self._get_name_from_selection("label_third"),
            )
        elif self.label_second:
            class_name += ", ({})".format(self._get_name_from_selection("label_second"))

        if self.packaging_group:
            class_name += ", {}".format(
                self._get_name_from_selection("packaging_group")
            )

        if self.tunnel_code:
            class_name += ", {}".format(self._get_name_from_selection("tunnel_code"))

        if self.envir_hazardous == "yes":
            class_name += ", {}".format(_("Environmentally hazardous"))

        return class_name

    def _get_name_from_selection(self, field_name):
        temp_dict = dict(self._fields[field_name].selection)
        return temp_dict.get(getattr(self, field_name))
