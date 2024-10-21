# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    "name": "l10n Eu Product Adr Dangerous Goods",
    "version": "18.0.1.0.0",
    "category": "Inventory/Delivery",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "maintainers": ["mmequignon"],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "depends": ["l10n_eu_product_adr"],
    "data": [
        # data
        "data/utility_models.xml",
        # security
        "security/ir.model.access.csv",
        # views
        "views/product_product.xml",
    ],
}
