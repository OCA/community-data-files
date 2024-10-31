# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    "name": "Base UNECE",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "license": "LGPL-3",
    "development_status": "Production/Stable",
    "summary": "Base module for UNECE code lists",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["astirpe", "alexis-via"],
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["base"],
    "data": ["views/unece_code_list.xml", "security/ir.model.access.csv"],
    "installable": True,
}
