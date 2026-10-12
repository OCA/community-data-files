This module provides the core data structure, views, security, and menus for managing ISO 7010 graphical symbols for safety signs within Odoo.

**Important:** This module only provides the *structure*. It does **not** contain any actual symbol data records or image files. To load symbols, you must install separate data modules, such as `base_iso7010_data_mandatory`, `base_iso7010_data_warning`, etc.

This module serves as a base dependency for other modules that need to load or reference standard ISO 7010 symbols.

## Key Features

* Defines the `iso7010.symbol` model with fields for ISO code, name, description, category (mandatory, warning, etc.), and image.
* Provides basic views (list, form, search) for managing these symbols.
* Adds a menu item under Settings > Technical > ISO Standards > ISO 7010 Symbols (visible to Administrators).
* Includes necessary access control rules.
