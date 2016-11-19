# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Account Tax UNECE',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'UNECE nomenclature for taxes',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['account', 'base_unece'],
    'data': [
        'views/account_tax.xml',
        'data/unece_tax_type.xml',
        'data/unece_tax_categ.xml',
        ],
    'installable': True,
}
