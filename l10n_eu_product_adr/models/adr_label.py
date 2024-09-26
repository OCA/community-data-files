# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# Copyright 2021 Stefan Rijnhart <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models
from odoo.exceptions import ValidationError


class AdrLabel(models.Model):
    _name = "adr.label"
    _description = "Dangerous Goods Label"
    _order = "code, name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    image = fields.Binary(required=True)
    class_id = fields.Many2one(comodel_name="adr.class", string="Class", required=True)
    goods_ids = fields.Many2many(
        comodel_name="adr.goods",
        copy=False,
        string="ADR Goods",
        help="The dangerous goods to which this label is applied",
    )

    def unlink(self):
        """Restrict removal of labels in use"""
        for label in self:
            if label.goods_ids:
                raise ValidationError(
                    self.env._(
                        "Dangerous Goods Label %(label)s cannot be deleted because it "
                        "is in use on one or more dangerous goods: %(labels)s",
                        label=label.name,
                        labels=", ".join(label.goods_ids.mapped("un_number")),
                    )
                )
        return super().unlink()
