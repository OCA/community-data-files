# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductFaoFishingTechnique(models.Model):
    _name = "product.fao.fishing.technique"
    _description = "Fishing Technique"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"
    _order = "parent_path"

    name = fields.Char(string="Name", index=True, required=True, translate=True)
    complete_name = fields.Char(
        "Complete Name", compute="_compute_complete_name", store=True
    )
    parent_id = fields.Many2one(
        comodel_name="product.fao.fishing.technique",
        string="Parent Technique",
        index=True,
        ondelete="cascade",
    )
    child_id = fields.One2many(
        comodel_name="product.fao.fishing.technique",
        inverse_name="parent_id",
        string="Child Technique",
    )
    parent_path = fields.Char(index=True)

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for tech in self:
            if tech.parent_id:
                tech.complete_name = "{} / {}".format(
                    tech.parent_id.complete_name, tech.name
                )
            else:
                tech.complete_name = tech.name

    @api.constrains("parent_id")
    def _check_technique_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_("Error ! You cannot create recursive techniques."))
        return True
