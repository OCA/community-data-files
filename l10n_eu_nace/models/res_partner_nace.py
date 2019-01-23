# Copyright 2019 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ResPartnerNace(models.Model):
    _name = 'res.partner.nace'
    _description = 'European NACE partner categories'
    _order = "code"
    _parent_order = "name"
    _parent_store = True

    name = fields.Char(required=True, translate=True)
    level = fields.Integer(required=True)
    code = fields.Char(required=True)
    generic = fields.Char(string="ISIC Rev.4")
    rules = fields.Text()
    central_content = fields.Text(translate=True, string="Contents")
    limit_content = fields.Text(translate=True, string="Also contents")
    exclusions = fields.Char(translate=True, string="Excludes")
    parent_id = fields.Many2one(
        'res.partner.nace', string="Parent Code", ondelete='restrict')
    child_ids = fields.One2many(
        'res.partner.nace', 'parent_id', string="NACE subcategories")
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("ref_code", "unique (code)", "NACE Code must be unique!")
    ]

    @api.multi
    def name_get(self):
        res = []
        for category in self:
            if self.env.context.get('nace_display') == 'long':
                names = []
                current = category
                while current:
                    if current.code:
                        names.append("[%s] %s" % (current.code, current.name))
                    else:
                        names.append(current.name)
                    current = current.parent_id
                res.append((category.id, ' / '.join(reversed(names))))
            else:
                res.append(
                    (category.id, "[%s] %s" % (category.code, category.name))
                )
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        return self.search(
            ['|', ('name', operator, name), ('code', 'ilike', name)]
        ).name_get()
