# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product UoM UNECE",
    "version": "17.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "development_status": "Production/Stable",
    "summary": "UNECE nomenclature for the units of measure",
    "author": "Akretion,Odoo Community Association (OCA)",
    "maintainers": ["astirpe", "alexis-via"],
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["uom"],
    "data": ["data/unece.xml", "views/uom_uom.xml", "views/uom_category.xml"],
    "installable": True,
}
