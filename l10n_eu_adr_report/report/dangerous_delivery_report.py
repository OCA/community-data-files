# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class DangerousDeliveryADR(models.AbstractModel):
    _name = 'report.l10n_eu_adr_report.report_delivery_dangerous'
    _description = "Dangerous Delivery Report ADR"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking']
        data = data or {}
        docs = self.env['stock.picking'].browse(docids)
        lines = self._prepare_dangerous_lines(docs)
        docargs = {
            'doc_ids': docs.ids,
            'doc_model': 'stock.picking',
            'docs': docs,
            'data': data.get('form', False),
            # Amount of 7 lines is to satisfy requirements for first page
            # as this amount is fiting A4 page
            'first_page_lines': lines[:7],
            'next_page_lines': lines[7:],
        }
        return docargs

    def _prepare_dangerous_lines(self, pickings):
        vals = []
        pickings.ensure_one()
        for move_line in pickings.move_line_ids:
            if move_line.product_id.dangerous_component_ids:
                vals += self._get_dangerous_class_line_vals(move_line)
            elif move_line.product_id.dangerous_class_id:
                vals += self._get_dangerous_component_line_vals(move_line)
        return vals

    def _get_dangerous_class_line_vals(self, move):
        vals = []
        for component in move.product_id.dangerous_component_ids:
            product = component.component_product_id
            vals.append(
                {
                    'name': product.name,
                    'class': product.get_full_class_name(),
                    'division': component.dangerous_class_id.class_type_id.division,
                    'weight': component.weight
                    * move.qty_done,
                    'volume': component.volume
                    * move.qty_done,
                    'gross_weight': move.move_id.weight,
                }
            )
        return vals

    def _get_dangerous_component_line_vals(self, move):
        product = move.product_id.product_tmpl_id
        vals = []
        vals.append({
            'name': product.name,
            'class': product.get_full_class_name(),
            'division': product.dangerous_class_id.class_type_id.division,
            'weight': move.qty_done,
            'volume': move.qty_done,
            'gross_weight': move.move_id.weight,
        })
        return vals
