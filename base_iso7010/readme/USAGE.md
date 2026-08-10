This module primarily provides the backend structure and is intended as a dependency for data-loading or integration modules.

**Viewing Symbol Structure (Administrator):**

1.  Log in as an Administrator.
2.  Navigate to Settings > Technical > ISO Standards > ISO 7010 Symbols.
3.  You will see the list view defined for symbols. This list will be empty until you install one or more data modules (e.g., `base_iso7010_data_mandatory`).

**Developer Usage:**

* Other modules should add `base_iso7010` to their dependencies.
* Use Many2one or Many2many fields in your custom models linking to the `iso7010.symbol` model to reference safety symbols. Example:
    ```python
    from odoo import fields, models

    class MyModel(models.Model):
        _name = 'my.model'

        required_symbol_id = fields.Many2one('iso7010.symbol', string='Required Symbol')
        applicable_symbols_ids = fields.Many2many('iso7010.symbol', string='Applicable Symbols')
    ```
* Ensure that appropriate `base_iso7010_data_*` modules are also installed in the target database to provide the necessary symbol records for selection in your custom fields.
