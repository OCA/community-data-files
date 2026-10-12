This is a developer-facing module — it has no UI of its own.

To resolve a supplier UoM code, call :meth:`uom.preset._resolve`:

```python
uom = self.env["uom.preset"]._resolve("pricat", "STU")
# -> uom.uom record whose unece_code == "C62", or empty recordset on miss.
```

Resolution is **strict**: an unknown vocabulary or a code missing from
the chosen vocabulary returns an empty recordset. The caller is
expected to chain its own fallback (typically ``uom_unece`` lookup, then
a default UoM).

To add a new vocabulary, create a small module that depends on
``uom_preset`` and inherits the abstract model:

```python
from odoo import api, models


class UomPreset(models.AbstractModel):
    _inherit = "uom.preset"

    @api.model
    def _uom_preset_vocabularies(self):
        vocabularies = super()._uom_preset_vocabularies()
        vocabularies["my_vocab"] = {
            "<supplier-code>": "<unece-code>",
            # ...
        }
        return vocabularies

    @api.model
    def _uom_preset_selection(self):
        selection = super()._uom_preset_selection()
        selection.append(("my_vocab", self.env._("My supplier vocabulary")))
        return selection
```

Vocabulary keys are uppercased before lookup, so it doesn't matter
how the supplier sends them.
