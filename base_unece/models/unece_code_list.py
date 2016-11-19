# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


# There are so many UNCL that can be usefull in Odoo
# that it would be stupid to have one object for each UNCL
# because it would duplicate the python code, views, menu entries, ACL, etc...
# So I decided to have a single object with a type field
class UneceCodeList(models.Model):
    _name = 'unece.code.list'
    _description = 'UNECE nomenclatures'
    _rec_name = 'display_name'
    _order = 'type, code'

    @api.multi
    @api.depends('code', 'name')
    def compute_display_name(self):
        for entry in self:
            entry.display_name = '[%s] %s' % (entry.code, entry.name)

    code = fields.Char(string='Code', required=True, copy=False)
    name = fields.Char(string='Name', required=True, copy=False)
    display_name = fields.Char(
        compute='compute_display_name', store=True, string='Display Name')
    type = fields.Selection([], string='Type', required=True)
    description = fields.Text(string='Description')

    _sql_constraints = [(
        'type_code_uniq',
        'unique(type, code)',
        'An UNECE code of the same type already exists'
        )]
