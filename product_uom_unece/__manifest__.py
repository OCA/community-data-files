# Copyright 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Product UoM UNECE',
    'version': '11.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'UNECE nomenclature for the units of measure',
    'author': 'Akretion,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/community-data-files/',
    'depends': ['product'],
    'data': [
        'data/unece.xml',
        'views/product_uom.xml',
        ],
    'installable': True,
}
