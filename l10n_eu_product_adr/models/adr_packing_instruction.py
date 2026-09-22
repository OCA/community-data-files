# Copyright 2021 Stefan Rijnhart <stefan@opener.amsterdam>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class AdrPackingInstruction(models.Model):
    _name = "adr.packing.instruction"
    _description = "Dangerous Goods Packing Instruction"
    _rec_name = "code"
    _order = "code"

    name = fields.Char(translate=True)
    code = fields.Char(required=True)
