# Copyright 2020 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from itertools import groupby

from odoo import fields, models

from odoo.addons.l10n_eu_product_adr.models.common import category_points_factor_map

# ADR 1.1.3.6 exemption threshold, in transport points
POINTS_LIMIT = 1000.0

# Transport categories of the ADR 1.1.3.6.3 table
TRANSPORT_CATEGORIES = ("0", "1", "2", "3", "4")


class DGProductCounter(models.TransientModel):
    _name = "dangerous.goods.handler"
    _description = "Wizard to count and prepare data for dangerous goods report"

    picking_ids = fields.Many2many("stock.picking", string="Pickings")

    def prepare_DG_data(self):
        """
        Result is lines for dangerous products
        :return: dict
        {'dg_lines':[{
                'product': product.product(40,),
                'dg_unit': 'kg (Kilogramm)',
                'class': 'UN UN Number, ...
                'packaging_type': adr.packing.instruction(6,),
                'qty_amount': 100.0,
                'product_weight': 10.0,
                'column_index': '3',
                'dangerous_amount': 1000.0
            }],
        'total_section':{
            'total_units': {'0': 0, '1': 0, '2': 1000.0, '3': 0, '4': 0},
            'factor': {'0': 0.0, '1': 50.0, '2': 3.0, '3': 1.0, '4': 0.0},
            'mass_points': {'0': 0.0, '1': 0.0, '2': 3000.0, '3': 0.0, '4': 0.0},
            'total_points': 3000.0,
            'warn': True
            }
        }
        """
        vals = {
            "dg_lines": [],
            "total_section": {},
        }
        for pick in self.picking_ids:
            if pick.state == "done":
                moves = pick.move_ids.filtered(lambda move: move.state == "done")
            else:
                moves = pick.move_ids
            dangerous_moves = moves.filtered(lambda move: move.product_id.is_dangerous)
            grouped_moves = groupby(
                sorted(dangerous_moves, key=lambda move: move.product_id.id),
                lambda move: move.product_id,
            )
            vals["dg_lines"] += self._get_DG_move_line_vals(grouped_moves)

        vals["total_section"] = self._compute_points_per_product(vals["dg_lines"])
        vals["total_section"]["total_points"] = self._compute_total_points(
            vals["total_section"]
        )
        vals["total_section"]["warn"] = self._is_limit_exceeded(vals["total_section"])
        return vals

    def _compute_points_per_product(self, vals):
        index = dict.fromkeys(TRANSPORT_CATEGORIES, 0.0)
        total_vals = {
            "total_units": index.copy(),
            "factor": index.copy(),
            "mass_points": index.copy(),
            "total_points": 0.0,
        }
        self._init_total_vals(total_vals)

        for k in index.keys():
            total_vals["total_units"][k] = self._sum_values(vals, "dangerous_amount", k)
            total_vals["mass_points"][k] = self._apply_rounding(
                total_vals["total_units"][k] * total_vals["factor"][k]
            )
        return total_vals

    def _sum_values(self, vals, field, index):
        return sum([item[field] for item in vals if item["column_index"] == index])

    def _compute_total_points(self, vals):
        return self._apply_rounding(sum(vals["mass_points"].values()))

    def _apply_rounding(self, amount):
        # should follow precision on product
        return round(amount, 1)

    def _is_limit_exceeded(self, vals):
        if vals["total_points"] > POINTS_LIMIT:
            return True
        return False

    def _init_total_vals(self, vals):
        # ADR 1.1.3.6.3 multiplication factors, per transport category
        vals["factor"].update(category_points_factor_map)

    def _get_DG_move_line_vals(self, moves):
        # unit measurement on stock is not considered
        result = []
        for product, move_lines in moves:
            qty = 0
            for rec in move_lines:
                if rec.state == "done":
                    qty += rec.quantity
                else:
                    qty += rec.product_uom_qty
            packaging_type = product.adr_packing_instruction_ids[:1]
            dg_unit = product.adr_limited_quantity_uom_id.name
            amount = qty * product.weight
            class_name = self._get_full_class_name(product)
            class_name += f", {qty}, {packaging_type.name}, {amount}, {dg_unit}"
            result.append(
                {
                    "product": product,
                    "dg_unit": dg_unit,
                    "class": class_name,
                    "packaging_type": packaging_type,
                    "qty_amount": qty,
                    "product_weight": product.weight,
                    "column_index": product.adr_transport_category,
                    "dangerous_amount": amount,
                }
            )

        return result

    def _get_full_class_name(self, product):
        """Return the designation of the goods, as printed on the form"""
        adr_goods = product.adr_goods_id
        class_name = f"UN {adr_goods.un_number}, {adr_goods.name}"
        labels = adr_goods.label_ids
        if labels:
            class_name += ", ({})".format(", ".join(labels.mapped("name")))
        return class_name
