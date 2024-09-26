# Copyright 2021 Opener B.V.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import Form, tagged

from odoo.addons.stock.tests.common import TestStockCommon


@tagged("post_install", "-at_install")
class TestAdrPoints(TestStockCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # On the Unit product, set the weight in kilos to determine the ADR quantity
        # This product from transport category exceptionally has a factor or 20, not 50
        cls.UnitA.adr_goods_id = cls.env.ref("l10n_eu_product_adr.adr_goods_0081")
        cls.UnitA.weight = 10.0
        # Second product is a product in kilos
        cls.kgB.adr_goods_id = cls.env.ref("l10n_eu_product_adr.adr_goods_0066")
        # Third product is a product in grams
        cls.gB.adr_goods_id = cls.env.ref("l10n_eu_product_adr.adr_goods_0066")
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )

    def test_adr_points(self):
        form = Form(self.env["stock.picking"], view="stock.view_picking_form")
        form.picking_type_id = self.warehouse.out_type_id
        with form.move_ids_without_package.new() as move:
            move.product_id = self.UnitA
            move.product_uom_qty = 2
        with form.move_ids_without_package.new() as move:
            move.product_id = self.kgB
            move.product_uom_qty = 3
        with form.move_ids_without_package.new() as move:
            move.product_id = self.gB
            move.product_uom_qty = 5000
        picking = form.save()
        # Qty 2 * weight 10 * factor 20
        self.assertEqual(picking.move_ids[0].adr_points, 400)
        # UoM qty 3 * factor 3
        self.assertEqual(picking.move_ids[1].adr_points, 9)
        # UoM qty 5000 / UoM factor 1000 * factor 3
        self.assertEqual(picking.move_ids[2].adr_points, 15)
        self.assertEqual(picking.adr_points, 424)
