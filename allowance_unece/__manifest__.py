# Copyright 2020 Decodio Applications (<http://decod.io>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Base UBL allowance",
    'version': "12.0.1.0.0",
    "author": "Decodio Applications, Odoo Community Association (OCA)",
    "development_status": "RC",
    "summary": "Discount codes for UBL",
    'website': "https://github.com/OCA/edi",
    'license': "LGPL-3",
    'depends': [
        "base_unece"
    ],
    'data': [
        "data/unece_allowance.xml"
    ],
    'installable': True,
}
