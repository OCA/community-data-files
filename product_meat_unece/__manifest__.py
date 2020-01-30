# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Meat Unece",
    "summary": """
        This module adds the UNECE Meat Carcasses and Cuts Classification.""",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "depends": [
        # Odoo
        "product",
        # OCA
        "base_unece",
    ],
    "data": ["data/unece_code_list.xml", "views/product_template.xml"],
}
