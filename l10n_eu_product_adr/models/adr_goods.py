# Copyright 2021 Stefan Rijnhart <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND

from .common import TRANSPORT_CATEGORIES, TUNNEL_RESTRICTION_CODES


class AdrGoods(models.Model):
    _name = "adr.goods"
    _description = "Dangerous Goods"

    active = fields.Boolean(default=True)
    un_number = fields.Char(
        string="UN Number",
        required=True,
        help=(
            "Contains the UN number: of the dangerous substance or article "
            "if the substance or article has been assigned its own specific "
            "UN number; or of the generic or n.o.s. entry to which the "
            "dangerous substances or articles not mentioned by name shall "
            "be assigned in accordance with the criteria ('decision trees') "
            "of Part 2."
        ),
    )
    name = fields.Char(
        "Name and description",
        required=True,
        translate=True,
        help=(
            "Contains, in upper case characters, the name of the substance or "
            "article, if the substance or article has been assigned its own "
            "specific UN number, or of the generic or n.o.s. entry to which "
            "it has been assigned in accordance with the criteria "
            "('decision trees') of Part 2. This name shall be used as the "
            "proper shipping name or, when applicable, as part of the proper "
            "shipping name (see 3.1.2 for further details on the proper "
            "shipping name)."
        ),
    )
    class_id = fields.Many2one(comodel_name="adr.class", string="Class", required=True)
    classification_code = fields.Char()
    label_ids = fields.Many2many(
        comodel_name="adr.label",
        string="Labels",
        help=(
            "The labels/placards (see 5.2.2.2 and 5.3.1.7) that have to be affixed "
            "to packages, containers, tank-containers, portable tanks, MEGCs and "
            "vehicles.)"
        ),
    )
    limited_quantity = fields.Float(digits="Product Unit of Measure")
    limited_quantity_uom_id = fields.Many2one("uom.uom", string="Limited Quantity UoM")
    packing_instruction_ids = fields.Many2many(
        comodel_name="adr.packing.instruction",
        string="Packing Instructions",
    )
    transport_category = fields.Selection(
        TRANSPORT_CATEGORIES,
        required=True,
    )
    tunnel_restriction_code = fields.Selection(
        TUNNEL_RESTRICTION_CODES,
        required=True,
    )

    @api.constrains("un_number")
    def _check_un_number(self):
        for goods in self:
            if len(goods.un_number) != 4:
                raise ValidationError(
                    self.env._(
                        "UN Number %s is invalid because it does not have "
                        "a length of 4.",
                        goods.un_number,
                    )
                )

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """Allow to search for UN Number"""
        args = list(args or [])
        if name and operator in ("ilike", "="):
            record = self.search(
                AND([args, [("un_number", operator, name)]]), limit=limit
            )
            if record:
                return [(rec.id, rec.display_name) for rec in record]
        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    @api.depends(
        "un_number",
        "name",
        "transport_category",
        "limited_quantity",
        "limited_quantity_uom_id",
    )
    def _compute_display_name(self):
        """Format the class name"""
        for rec in self:
            name = f"{rec.un_number} {rec.name}"
            affixes = []
            if rec.transport_category != "-":
                affixes.append(self.env._("cat:%s", rec.transport_category))
            if rec.limited_quantity:
                affixes.append(
                    self.env._(
                        "qty:%(limited_quantity)s %(limited_quantity_uom_id)s",
                        limited_quantity=rec.limited_quantity,
                        limited_quantity_uom_id=rec.limited_quantity_uom_id.name,
                    )
                )
            if affixes:
                name += f" ({', '.join(affixes)})"

            rec.display_name = name
