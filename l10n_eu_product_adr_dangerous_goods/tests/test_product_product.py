from odoo.addons.base.tests.common import BaseCommon


class TestProductProduct(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create test data for related models
        cls.limited_amount = cls.env["limited.amount"].create(
            {"name": "Test Limited Amount"}
        )
        cls.dg_unit = cls.env["dangerous.uom"].create({"name": "Test Dangerous UoM"})
        cls.storage_class = cls.env["storage.class"].create(
            {"name": "Test Storage Class"}
        )
        cls.packaging_type = cls.env["packaging.type"].create(
            {"name": "Test Packaging Type"}
        )
        cls.storage_temp = cls.env["storage.temp"].create({"name": "Test Storage Temp"})
        cls.wgk_class = cls.env["wgk.class"].create({"name": "Test WGK Class"})

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "limited_amount_id": cls.limited_amount.id,
                "content_package": 10.12345,
                "dg_unit": cls.dg_unit.id,
                "nag": "Test NAG",
                "veva_code_empty": "123-Empty",
                "veva_code_full": "456-Full",
                "storage_class_id": cls.storage_class.id,
                "packaging_type_id": cls.packaging_type.id,
                "storage_temp_id": cls.storage_temp.id,
                "flash_point": "-10",
                "wgk_class_id": cls.wgk_class.id,
                "h_no": "H12345",
                "envir_hazardous": "yes",
                "packaging_group": "3",
                "hazard_ind": "Hazard123",
                "voc": "15.5",
                "label_first": "1",
                "label_second": "3",
                "label_third": "5",
            }
        )

    def test_create_product(self):
        """Test creating a product with all the custom fields."""
        # Assert field values
        self.assertEqual(
            self.product.limited_amount_id,
            self.limited_amount,
            "Limited amount ID does not match the expected value",
        )
        self.assertEqual(
            self.product.content_package,
            10.12345,
            "Content package value does not match the expected value",
        )
        self.assertEqual(
            self.product.dg_unit,
            self.dg_unit,
            "DG unit does not match the expected value",
        )
        self.assertEqual(
            self.product.nag, "Test NAG", "NAG value does not match the expected value"
        )
        self.assertEqual(
            self.product.veva_code_empty,
            "123-Empty",
            "VEVA code empty does not match the expected value",
        )
        self.assertEqual(
            self.product.veva_code_full,
            "456-Full",
            "VEVA code full does not match the expected value",
        )
        self.assertEqual(
            self.product.storage_class_id,
            self.storage_class,
            "Storage class ID does not match the expected value",
        )
        self.assertEqual(
            self.product.packaging_type_id,
            self.packaging_type,
            "Packaging type does not match the expected value",
        )
        self.assertEqual(
            self.product.storage_temp_id,
            self.storage_temp,
            "Storage temperature does not match the expected value",
        )
        self.assertEqual(
            self.product.flash_point,
            "-10",
            "Flash point does not match the expected value",
        )
        self.assertEqual(
            self.product.wgk_class_id,
            self.wgk_class,
            "WGK class does not match the expected value",
        )
        self.assertEqual(
            self.product.h_no, "H12345", "H number does not match the expected value"
        )
        self.assertEqual(
            self.product.envir_hazardous,
            "yes",
            "Environmental hazardous flag does not match the expected value",
        )
        self.assertEqual(
            self.product.packaging_group,
            "3",
            "Packaging group does not match the expected value",
        )
        self.assertEqual(
            self.product.hazard_ind,
            "Hazard123",
            "Hazard indicator does not match the expected value",
        )
        self.assertEqual(
            self.product.voc, "15.5", "VOC value does not match the expected value"
        )
        self.assertEqual(
            self.product.label_first,
            "1",
            "First label value does not match the expected value",
        )
        self.assertEqual(
            self.product.label_second,
            "3",
            "Second label value does not match the expected value",
        )
        self.assertEqual(
            self.product.label_third,
            "5",
            "Third label value does not match the expected value",
        )

    def test_update_product(self):
        """Test updating a product's custom fields."""
        product_test = self.env["product.product"].create(
            {
                "name": "Test Product",
                "envir_hazardous": "no",
            }
        )

        # Update fields
        product_test.write(
            {
                "envir_hazardous": "yes",
                "label_first": "2",
            }
        )

        # Assert updates
        self.assertEqual(
            product_test.envir_hazardous,
            "yes",
            "Environmental hazardous flag should be 'yes' but is not.",
        )
        self.assertEqual(
            product_test.label_first, "2", "First label value should be '2' but is not."
        )
