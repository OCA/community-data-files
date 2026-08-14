# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "Account Tax UNECE",
    "version": "15.0.2.0.0",
    "category": "Accounting & Finance",
    "license": "AGPL-3",
    "development_status": "Production/Stable",
    "summary": "UNECE nomenclature for taxes",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["alexis-via"],
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["account", "base_unece"],
    "data": [
        "views/account_tax.xml",
        "views/account_tax_template.xml",
        "views/unece_code_list.xml",
        "data/unece_tax_type.xml",
        "data/unece_tax_categ.xml",
        "data/unece_tax_vatex.xml",
    ],
    "installable": True,
}
