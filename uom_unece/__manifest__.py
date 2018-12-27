# Copyright 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'UoM UNECE',
    'version': '12.0.1.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'UNECE nomenclature for the units of measure',
    'author': 'Akretion, '
              'Shine IT<contact@openerp.cn>, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/community-data-files/',
    'depends': ['uom'],
    'data': [
        'data/unece.xml',
        'views/uom_uom_view.xml',
    ],
    'installable': True,
}
