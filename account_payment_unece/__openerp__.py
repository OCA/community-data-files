# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Account Payment UNECE',
    'version': '8.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'UNECE nomenclature for the payment mode types',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': ['account_banking_payment_export', 'base_unece'],
    'data': [
        'data/unece.xml',
        'views/payment_mode_type.xml',
        ],
    'installable': True,
}
