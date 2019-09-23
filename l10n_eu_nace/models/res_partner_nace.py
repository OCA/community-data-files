# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResPartnerNace(models.Model):

    _name = 'res.partner.nace'
    _description = 'European NACE partner category'
    _order = 'code'
    _parent_store = True

    name = fields.Char(index=True, translate=True)
    parent_id = fields.Many2one(comodel_name="res.partner.nace", index=True)
    code = fields.Char(index=True)
    child_ids = fields.One2many(
        'res.partner.nace', 'parent_id', string='NACE subcategories'
    )
    active = fields.Boolean(index=True, default=True)
    parent_path = fields.Char(index=True)
    partner_ids = fields.One2many(
        comodel_name="res.partner", inverse_name="nace_id", string="Partners"
    )

    @api.multi
    def name_get(self):
        res = []
        for category in self:
            if self._context.get('nace_display') == 'short':
                res.append(
                    (category.id, "[%s] %s" % (category.code, category.name))
                )
            else:
                names = []
                current = category
                while current:
                    if current.code:
                        names.append("[%s] %s" % (current.code, current.name))
                    else:
                        names.append(current.name)
                    current = current.parent_id
                res.append((category.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = list(args or [])
        if not (name == "" and operator == "ilike"):
            args += ["|"]
        args += [("code", operator, name)]
        return super().name_search(name, args, operator, limit)

    _sql_constraints = [
        ("ref_code", "unique (code)", _("NACE Code must be unique!"))
    ]
