# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    unece_type_id = fields.Many2one(
        'unece.code.list', string='UNECE Tax Type',
        domain=[('type', '=', 'tax_type')],
        help="Select the Tax Type Code of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement 5153")
    unece_type_code = fields.Char(
        related='unece_type_id.code', store=True,
        string='UNECE Type Code')
    unece_categ_id = fields.Many2one(
        'unece.code.list', string='UNECE Tax Category',
        domain=[('type', '=', 'tax_categ')],
        help="Select the Tax Category Code of the official "
        "nomenclature of the United Nations Economic "
        "Commission for Europe (UNECE), DataElement 5305")
    unece_categ_code = fields.Char(
        related='unece_categ_id.code', store=True,
        string='UNECE Category Code')
