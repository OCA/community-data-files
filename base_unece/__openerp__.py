# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Base UNECE',
    'version': '8.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Base module for UNECE code lists',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'views/unece_code_list.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
