# Copyright 2026 ACSONE SA/NV
# Copyright 2026 BCIM
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Packaging UNECE",
    "summary": """UNECE nomenclature for product packaging""",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV, BCIM, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "depends": ["product_packaging_level", "base_unece"],
    "maintainers": ["sbejaoui", "jbaudoux"],
    "data": [
        "data/unece_code_list.xml",
        "views/unece_code_list.xml",
        "views/product_packaging_level.xml",
    ],
}
