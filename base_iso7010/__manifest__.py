{
    "name": "Base ISO 7010 Symbols Structure",
    "version": "18.0.1.0.0",
    "summary": """
        This module provides the core structure (model, views, security, menus)
        for managing ISO 7010 safety symbols.

        It does NOT contain any actual symbol data records. Install separate
        'base_iso7010_data_*' modules to load symbol data for specific categories
        (e.g., base_iso7010_data_mandatory).
    """,
    "author": "bosd, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/iso7010_symbol_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
