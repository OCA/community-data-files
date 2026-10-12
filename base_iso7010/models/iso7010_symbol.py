from odoo import fields, models


class Iso7010Symbol(models.Model):
    _name = "iso7010.symbol"
    _description = "ISO 7010 Safety Symbol"
    _order = "iso_code"

    name = fields.Char(
        required=True,
        translate=True,
        help="Meaning of the symbol, e.g., 'Wear eye protection'.",
    )
    description = fields.Text(
        translate=True,
        help="Optional further details about the symbol or its usage.",
    )
    iso_code = fields.Char(
        required=True,
        readonly=True,
        copy=False,
        index=True,
        help="The official ISO 7010 code, e.g., M001, W002, P003, E001, F001.",
    )
    category = fields.Selection(
        [
            ("mandatory", "Mandatory Action (Blue Circle)"),
            ("warning", "Warning (Yellow Triangle)"),
            ("prohibition", "Prohibition (Red Circle with Slash)"),
            ("emergency", "Emergency Escape/First-Aid (Green Square)"),
            ("fire", "Fire Equipment (Red Square)"),
            ("supplementary", "Supplementary (Usually Rectangular)"),
        ],
        required=True,
        index=True,
        readonly=True,
    )
    image = fields.Image(
        string="Symbol Image",
        max_width=256,  # Define max width/height for storage variants
        max_height=256,
        readonly=True,  # Data loaded from files
        help="Image representation of the symbol (preferably SVG).",
    )
    active = fields.Boolean(default=True, index=True)

    _sql_constraints = [
        ("iso_code_uniq", "unique(iso_code)", "ISO Code must be unique!")
    ]

    def name_get(self):
        """Include ISO code in the display name"""
        res = []
        for record in self:
            name = f"[{record.iso_code}] {record.name}"
            res.append((record.id, name))
        return res
