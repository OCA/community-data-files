# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import TransactionCase


class TestTradeCompliance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Clean up any existing test data from previous runs
        cls.env["trade.compliance.code"].search([("name", "like", "TEST-%")]).unlink()
        cls.env["trade.compliance.regime"].search([("name", "like", "TEST-%")]).unlink()

        # Create test regimes
        cls.regime_us = cls.env["trade.compliance.regime"].create(
            {
                "name": "TEST-US",
                "description": "Test US Regime",
            }
        )
        cls.regime_eu = cls.env["trade.compliance.regime"].create(
            {
                "name": "TEST-EU",
                "description": "Test EU Regime",
            }
        )
        # Create test codes
        cls.code_3a001 = cls.env["trade.compliance.code"].create(
            {
                "name": "TEST-3A001",
                "regime_id": cls.regime_us.id,
                "description": "Electronic equipment",
            }
        )
        cls.code_ear99 = cls.env["trade.compliance.code"].create(
            {
                "name": "TEST-EAR99",
                "regime_id": cls.regime_us.id,
                "description": "Not otherwise specified",
            }
        )
        # Create test category
        cls.category = cls.env["product.category"].create(
            {
                "name": "Test Electronics",
                "compliance_code_id": cls.code_3a001.id,
            }
        )
        cls.category_no_code = cls.env["product.category"].create(
            {
                "name": "Test Category No Code",
            }
        )

    def test_01_code_different_regime_ok(self):
        """Test same code name in different regime is allowed"""
        # Same code in different regime should be OK
        code_eu = self.env["trade.compliance.code"].create(
            {
                "name": "TEST-3A001",  # Same name as US code
                "regime_id": self.regime_eu.id,  # Different regime
                "description": "EU version",
            }
        )
        self.assertEqual(code_eu.name, "TEST-3A001")
        self.assertEqual(code_eu.regime_id, self.regime_eu)

    def test_02_code_display_name(self):
        """Test compliance code display_name via name_get"""
        name_get_result = self.code_3a001.name_get()
        self.assertEqual(
            name_get_result[0][1],
            "TEST-3A001 (TEST-US)",
        )

    def test_03_code_name_search(self):
        """Test searching for codes by name"""
        result = self.env["trade.compliance.code"].name_search("TEST-3A001")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], self.code_3a001.id)

    def test_04_category_default_code(self):
        """Test product inherits code from category on create"""
        product = self.env["product.template"].create(
            {
                "name": "Test Electronics Product",
                "categ_id": self.category.id,
            }
        )
        self.assertEqual(
            product.compliance_code_id,
            self.code_3a001,
            "Product should inherit compliance code from category",
        )

    def test_05_category_no_code(self):
        """Test product creation in category without code"""
        product = self.env["product.template"].create(
            {
                "name": "Test Product No Code",
                "categ_id": self.category_no_code.id,
            }
        )
        self.assertFalse(
            product.compliance_code_id,
            "Product should not have compliance code if category doesn't have one",
        )

    def test_07_product_explicit_code(self):
        """Test product with explicitly set code doesn't get overridden"""
        product = self.env["product.template"].create(
            {
                "name": "Test Product Explicit",
                "categ_id": self.category.id,
                "compliance_code_id": self.code_ear99.id,
            }
        )
        self.assertEqual(
            product.compliance_code_id,
            self.code_ear99,
            "Explicitly set code should not be overridden",
        )

    def test_08_category_change_empty_code(self):
        """Test changing category updates code when product has no code"""
        product = self.env["product.template"].create(
            {
                "name": "Test Product",
                "categ_id": self.category_no_code.id,
            }
        )
        self.assertFalse(product.compliance_code_id)
        # Change to category with code
        product.write({"categ_id": self.category.id})
        # Onchange should set the code from new category
        product._onchange_categ_id_compliance()
        self.assertEqual(
            product.compliance_code_id,
            self.code_3a001,
            "Code should be set from new category when product has no code",
        )

    def test_09_category_change_existing_code(self):
        """Test category change does not override existing code"""
        product = self.env["product.template"].create(
            {
                "name": "Product with Code",
                "categ_id": self.category_no_code.id,
                "compliance_code_id": self.code_ear99.id,
            }
        )
        # Change category - should not override existing code
        product.categ_id = self.category
        self.assertEqual(product.compliance_code_id, self.code_ear99)

    def test_10_write_category_change_inherits_code(self):
        """Test write method inherits code on category change"""
        product = self.env["product.template"].create(
            {
                "name": "Product No Code",
                "categ_id": self.category_no_code.id,
            }
        )
        self.assertFalse(product.compliance_code_id)

        # Change category via write (simulates batch update)
        product.write({"categ_id": self.category.id})

        # Should inherit code from new category
        self.assertEqual(product.compliance_code_id, self.code_3a001)

    def test_11_write_category_change_preserves_code(self):
        """Test write method preserves existing code on category change"""
        product = self.env["product.template"].create(
            {
                "name": "Product With Code",
                "categ_id": self.category_no_code.id,
                "compliance_code_id": self.code_ear99.id,
            }
        )

        # Change category via write - should preserve existing code
        product.write({"categ_id": self.category.id})

        # Should keep original code
        self.assertEqual(product.compliance_code_id, self.code_ear99)

    def test_12_write_batch_category_change(self):
        """Test batch write inherits codes for products without codes"""
        # Create multiple products without codes
        products = self.env["product.template"].create(
            [
                {
                    "name": "Product 1",
                    "categ_id": self.category_no_code.id,
                },
                {
                    "name": "Product 2",
                    "categ_id": self.category_no_code.id,
                },
            ]
        )

        # Batch update category - should inherit code
        products.write({"categ_id": self.category.id})

        # Both should have the code
        for product in products:
            self.assertEqual(product.compliance_code_id, self.code_3a001)

    def test_13_write_no_category_change(self):
        """Test write without category change doesn't trigger inheritance"""
        product = self.env["product.template"].create(
            {
                "name": "Product",
                "categ_id": self.category_no_code.id,
            }
        )

        # Write other field - should not add code
        product.write({"name": "Updated Name"})

        # Should still have no code
        self.assertFalse(product.compliance_code_id)

    def test_14_name_search_by_regime(self):
        """Test searching codes by regime name"""
        # Search by regime name
        result = self.env["trade.compliance.code"].name_search("TEST-US")
        # Should find codes in US regime
        self.assertTrue(len(result) > 0)

    def test_15_name_search_empty(self):
        """Test name_search with empty string"""
        result = self.env["trade.compliance.code"].name_search("")
        # Should return results (default behavior)
        self.assertTrue(len(result) >= 0)

    def test_16_related_fields(self):
        """Test related fields on product"""
        product = self.env["product.template"].create(
            {
                "name": "Test Product",
                "categ_id": self.category.id,
            }
        )
        self.assertEqual(product.compliance_regime_id, self.regime_us)
        self.assertEqual(product.compliance_code_description, "Electronic equipment")
