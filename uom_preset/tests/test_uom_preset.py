# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestUomPreset(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.UomPreset = cls.env["uom.preset"]
        # ``uom_unece`` data ships unece_code='C62' on uom.product_uom_unit
        # and 'KGM' on uom.product_uom_kgm.
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_kgm = cls.env.ref("uom.product_uom_kgm")

    # --- pricat -----------------------------------------------------

    def test_pricat_stu_resolves_to_unit(self):
        self.assertEqual(self.UomPreset._resolve("pricat", "STU"), self.uom_unit)

    def test_pricat_kgm_omitted_returns_empty(self):
        # Pricat ``KGM`` is dropped from the vocab because it equals the
        # UN/CEFACT Rec 20 code; callers resolve it via ``uom_unece`` directly.
        self.assertFalse(self.UomPreset._resolve("pricat", "KGM"))

    def test_pricat_lowercase_input(self):
        self.assertEqual(self.UomPreset._resolve("pricat", "stu"), self.uom_unit)

    def test_pricat_padded_input(self):
        self.assertEqual(self.UomPreset._resolve("pricat", "  STU  "), self.uom_unit)

    def test_pricat_unknown_code_returns_empty(self):
        self.assertFalse(self.UomPreset._resolve("pricat", "NOPE"))

    def test_pricat_collapses_packaging_to_unit(self):
        for code in ("PAK", "DOO", "SET", "PAA", "ROL", "DRU", "KIT"):
            self.assertEqual(
                self.UomPreset._resolve("pricat", code),
                self.uom_unit,
                f"Pricat code {code!r} should collapse to Units",
            )

    # --- x12_355 ----------------------------------------------------

    def test_x12_kg_resolves_to_kilogram(self):
        self.assertEqual(self.UomPreset._resolve("x12_355", "KG"), self.uom_kgm)

    def test_x12_pc_resolves_to_unit(self):
        # ANSI X12 'PC' = piece -> UN/CEFACT 'C62' (one/piece/unit).
        self.assertEqual(self.UomPreset._resolve("x12_355", "PC"), self.uom_unit)

    def test_x12_lowercase_input(self):
        self.assertEqual(self.UomPreset._resolve("x12_355", "kg"), self.uom_kgm)

    def test_x12_unknown_code_returns_empty(self):
        self.assertFalse(self.UomPreset._resolve("x12_355", "ZZZ"))

    # --- registry / generic -----------------------------------------

    def test_unknown_vocabulary_returns_empty(self):
        self.assertFalse(self.UomPreset._resolve("does-not-exist", "STU"))

    def test_empty_supplier_code_returns_empty(self):
        self.assertFalse(self.UomPreset._resolve("pricat", ""))
        self.assertFalse(self.UomPreset._resolve("pricat", None))

    def test_empty_vocabulary_returns_empty(self):
        self.assertFalse(self.UomPreset._resolve("", "STU"))
        self.assertFalse(self.UomPreset._resolve(None, "STU"))

    def test_selection_contains_all_vocabularies(self):
        keys = [k for k, _label in self.UomPreset._uom_preset_selection()]
        self.assertIn("pricat", keys)
        self.assertIn("x12_355", keys)

    def test_vocabularies_contains_all(self):
        vocabularies = self.UomPreset._uom_preset_vocabularies()
        self.assertIn("pricat", vocabularies)
        self.assertIn("x12_355", vocabularies)

    def test_no_pass_through_entries_in_vocabularies(self):
        """Pass-through entries (alias == unece_code) defeat the point of
        a vocabulary — callers can use ``uom_unece`` directly. Guard the
        invariant for both shipped vocabularies."""
        vocabularies = self.UomPreset._uom_preset_vocabularies()
        for name, vocab in vocabularies.items():
            for alias, unece_code in vocab.items():
                self.assertNotEqual(
                    alias, unece_code, f"{name}: {alias!r} is a pass-through"
                )
