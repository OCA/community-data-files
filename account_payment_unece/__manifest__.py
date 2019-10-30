# Copyright 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "Account Payment UNECE",
    "version": "13.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "summary": "UNECE nomenclature for the payment methods",
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["account_payment_mode", "base_unece"],
    "data": [
        "data/unece.xml",
        "data/account_payment_method.xml",
        "views/account_payment_method.xml",
    ],
    "installable": True,
}
