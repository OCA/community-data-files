# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "ADR Products Report",
    "summary": "Print Delivery report to ADR standart",
    "version": "13.0.1.0.2",
    "development_status": "Alpha",
    "category": "Product",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_eu_product_adr", "stock", "delivery"],
    "data": ["report/dangerous_good_delivery_report.xml", "views/assets.xml"],
    "demo": ["data/product_picking_demo.xml"],
}
