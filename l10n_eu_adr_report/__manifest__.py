# Copyright 2019 Camptocamp SA
# Copyright 2024 Odoo Community Association (OCA)
# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "ADR Products Report",
    "summary": "Print Delivery report to ADR standard",
    "version": "18.0.1.0.0",
    "category": "Inventory/Delivery",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Camptocamp, ACSONE SA/NV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["l10n_eu_product_adr", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "report/dangerous_good_delivery_report.xml",
    ],
    "demo": ["data/product_picking_demo.xml"],
    "assets": {
        "web.report_assets_common": [
            "l10n_eu_adr_report/static/src/scss/adr_report.scss",
        ],
    },
}
