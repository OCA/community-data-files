# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDangerousGoodsHandler(TransactionCase):
    """Data prepared by the wizard for the ADR form"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        # UN 1230 METHANOL, transport category 2 -> factor 3
        cls.goods = cls.env.ref("l10n_eu_product_adr.adr_goods_1230")
        cls.product = cls._create_product("Dangerous Product (test)", cls.goods)

    @classmethod
    def _create_product(cls, name, goods):
        return cls.env["product.product"].create(
            {
                "name": name,
                "type": "consu",
                "weight": 2.0,
                "uom_id": cls.uom_kg.id,
                "is_dangerous": bool(goods),
                "adr_goods_id": goods.id if goods else False,
            }
        )

    def _prepare_wizard_values(self, qty, product=None, done=False):
        """Return the wizard data for a picking of `qty` of `product`"""
        picking_type = self.env.ref("stock.picking_type_out")
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": picking_type.id,
                "location_id": picking_type.default_location_src_id.id,
                "location_dest_id": self.env.ref("stock.stock_location_customers").id,
            }
        )
        self.env["stock.move"].create(
            {
                "name": "test",
                "picking_id": picking.id,
                "product_id": (product or self.product).id,
                "product_uom_qty": qty,
                "product_uom": self.uom_kg.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
            }
        )
        if done:
            picking.action_confirm()
            picking.move_ids.quantity = qty
            picking.move_ids.picked = True
            picking._action_done()
        wizard = self.env["dangerous.goods.handler"].create(
            {"picking_ids": [(6, 0, picking.ids)]}
        )
        return wizard.prepare_DG_data()

    def test_dangerous_goods_line(self):
        """A dangerous product yields one line, weighed by its product weight"""
        lines = self._prepare_wizard_values(5.0)["dg_lines"]
        self.assertEqual(len(lines), 1)
        line = lines[0]
        self.assertEqual(line["qty_amount"], 5.0)
        self.assertEqual(line["product_weight"], 2.0)
        # 5 kg x 2.0 = 10.0
        self.assertEqual(line["dangerous_amount"], 10.0)
        self.assertEqual(line["column_index"], "2")
        self.assertIn("UN 1230", line["class"])

    def test_transport_points_below_the_limit(self):
        """Category 2 counts 3 points per kilo, and 30 points raise no warning"""
        totals = self._prepare_wizard_values(5.0)["total_section"]
        self.assertEqual(totals["factor"]["2"], 3)
        self.assertEqual(totals["total_units"]["2"], 10.0)
        # 10.0 x 3
        self.assertEqual(totals["mass_points"]["2"], 30.0)
        self.assertEqual(totals["total_points"], 30.0)
        self.assertFalse(totals["warn"])

    def test_transport_points_above_the_limit(self):
        """Past 1000 points, the ADR 1.1.3.6 exemption no longer applies"""
        # 200 kg x 2.0 x 3 = 1200
        totals = self._prepare_wizard_values(200.0)["total_section"]
        self.assertEqual(totals["total_points"], 1200.0)
        self.assertTrue(totals["warn"])

    def test_done_picking_reports_the_moved_quantity(self):
        """Once the transfer is done, the quantity actually moved is reported"""
        lines = self._prepare_wizard_values(5.0, done=True)["dg_lines"]
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["qty_amount"], 5.0)

    def test_picking_without_dangerous_goods(self):
        """A safe product is not reported and weighs no point"""
        safe_product = self._create_product("Safe Product (test)", False)
        data = self._prepare_wizard_values(5.0, product=safe_product)
        self.assertFalse(data["dg_lines"])
        self.assertEqual(data["total_section"]["total_points"], 0.0)
