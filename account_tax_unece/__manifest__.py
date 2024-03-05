# Copyright 2016-2020 Akretion France (http://www.akretion.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "Account Tax UNECE",
    "version": "17.0.1.0.0",
    "category": "Accounting & Finance",
    "license": "LGPL-3",
    "development_status": "Production/Stable",
    "summary": "UNECE nomenclature for taxes",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["account", "base_unece"],
    "data": [
        "views/account_tax.xml",
        "data/unece_tax_type.xml",
        "data/unece_tax_categ.xml",
    ],
    "installable": True,
}
