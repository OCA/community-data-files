# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import NEGATIVE_TERM_OPERATORS


class ResPartnerNace(models.Model):
    _name = "res.partner.nace"
    _description = "European NACE partner category"
    _order = "code"
    _parent_store = True
    _rec_name = "complete_name"

    complete_name = fields.Char(
        compute="_compute_complete_name", search="_search_complete_name"
    )
    name = fields.Char(index=True, translate=True)
    parent_id = fields.Many2one(comodel_name="res.partner.nace", index=True)
    code = fields.Char(index=True)
    child_ids = fields.One2many(
        "res.partner.nace", "parent_id", string="NACE subcategories"
    )
    active = fields.Boolean(index=True, default=True)
    parent_path = fields.Char(index=True)
    partner_ids = fields.One2many(
        comodel_name="res.partner", inverse_name="nace_id", string="Partners"
    )

    @api.depends("code", "name")
    def _compute_complete_name(self):
        for category in self:
            if self._context.get("nace_display") != "long":
                category.complete_name = "[%s] %s" % (category.code, category.name)
            else:
                names = []
                current = category
                while current:
                    if current.code:
                        names.append("[%s] %s" % (current.code, current.name))
                    else:
                        names.append(current.name)
                    current = current.parent_id
                category.complete_name = " / ".join(reversed(names))

    def _search_complete_name(self, operator, value):
        if operator in NEGATIVE_TERM_OPERATORS:
            domain = [
                "&",
                ("name", operator, value),
                ("code", operator, value),
            ]
        else:
            domain = [
                "|",
                ("name", operator, value),
                ("code", operator, value),
            ]
        return domain

    _sql_constraints = [("ref_code", "unique (code)", "NACE Code must be unique!")]
