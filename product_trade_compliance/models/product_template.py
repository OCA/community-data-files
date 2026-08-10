# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    compliance_code_id = fields.Many2one(
        comodel_name="trade.compliance.code",
        string="Compliance Code",
        help="Dual-Use or export control code for this product",
    )
    compliance_regime_id = fields.Many2one(
        comodel_name="trade.compliance.regime",
        string="Compliance Regime",
        related="compliance_code_id.regime_id",
        store=True,
        readonly=True,
    )
    compliance_code_description = fields.Text(
        string="Code Description",
        related="compliance_code_id.description",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Set compliance code from category if not explicitly provided."""
        for vals in vals_list:
            if "categ_id" in vals and "compliance_code_id" not in vals:
                category = self.env["product.category"].browse(vals["categ_id"])
                if category.compliance_code_id:
                    vals["compliance_code_id"] = category.compliance_code_id.id
        return super().create(vals_list)

    def write(self, vals):
        """Update compliance code when category changes (only if code not set)."""
        # If category is being changed
        if "categ_id" in vals:
            category = self.env["product.category"].browse(vals["categ_id"])
            # Only update products that don't have an explicit code set
            if category.compliance_code_id:
                for product in self.filtered(lambda prod: not prod.compliance_code_id):
                    # Add compliance_code_id to vals for this specific product
                    if len(self) == 1:
                        # Single record update
                        vals["compliance_code_id"] = category.compliance_code_id.id
                    else:
                        # Multiple records - update individually
                        product.compliance_code_id = category.compliance_code_id.id
        return super().write(vals)

    @api.onchange("categ_id")
    def _onchange_categ_id_compliance(self):
        """Set compliance code from category if product doesn't have one"""
        if self.categ_id and self.categ_id.compliance_code_id:
            if not self.compliance_code_id:
                self.compliance_code_id = self.categ_id.compliance_code_id
