# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Trade Compliance",
    "version": "18.0.1.0.0",
    "summary": "Manage Dual-Use (ECCN) and Trade Compliance codes (US/EU)",
    "category": "Inventory/Customs",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "development_status": "Beta",
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/trade_compliance_regime.xml",
        "data/trade.compliance.code.csv",
        "views/trade_compliance_regime_views.xml",
        "views/trade_compliance_code_views.xml",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
        "views/menu.xml",
    ],
}
