{
    "name": "Base ISO 7010 Symbols - Mandatory Data",
    "version": "18.0.1.0.0",
    "summary": """
        This module depends on 'base_iso7010' and loads the data records
        and SVG images for the 'Mandatory Action' category of ISO 7010 symbols.
    """,
    "author": "bosd, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/community-data-files",
    "category": "Extra Tools",
    "license": "LGPL-3",
    "depends": [
        "base_iso7010",
    ],
    "data": [
        "data/iso7010_mandatory_symbol_data.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
