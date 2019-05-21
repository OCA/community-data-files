# Copyright 2018 Eficent (https://www.eficent.com)
# @author: Jordi Ballester <jordi.ballester@eficent.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Base Currency ISO 4217',
    'version': '11.0.1.0.0',
    'category': 'Base',
    'license': 'AGPL-3',
    'summary': 'Adds numeric code, full name to currencies and number of '
               'digits, following the ISO 4217 specification',
    'author': 'Eficent,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/currency/',
    'depends': ['base'],
    'data': [
        'data/res.currency.csv',
        'views/res_currency_views.xml',
        ],
    'installable': True,
}
