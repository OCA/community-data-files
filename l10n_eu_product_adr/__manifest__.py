# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "ADR Products",
    "summary": "Allows to set appropriate danger class and components",
    "version": "13.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product", "sale", "stock"],
    "data": [
        "data/product_dangerous_type_data.xml",
        "data/product_dangerous_class_data.xml",
        "data/utility_models_data.xml",
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/product_dangerous.xml",
        "views/utility_models.xml",
    ],
}
