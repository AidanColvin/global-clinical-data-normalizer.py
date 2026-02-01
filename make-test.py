"""
make-test.py: Unified Edge Case Test Suite.

This script imports logic from the libraries and runs a "Gauntlet" of edge cases.
specifically focusing on the dangerous "Decimal Feet" trap and "Composite Stone" logic.

Usage:
    python make-test.py
"""

import unittest
# NOTE: These imports rely on the library files named 'weight_normalizer.py' 
# and 'height_normalizer.py'. Python does not allow hyphens in imports.
from weight_normalizer import parse_weight_to_lbs
from height_normalizer import parse_height_to_us, format_height

class TestClinicalEdgeCases(unittest.TestCase):
    
    # --- WEIGHT GAUNTLET ---
    
    def test_weight_composites(self):
        """Validates the '11 stone 6' logic."""
        # 11st (154) + 6lb = 160.0
        self.assertEqual(parse_weight_to_lbs("11st 6lb"), 160.0)
        self.assertEqual(parse_weight_to_lbs("11-6"), 160.0)
        # Should handle spaces
        self.assertEqual(parse_weight_to_lbs("11 stone 6"), 160.0)

    def test_weight_typos_and_slang(self):
        """Validates misspelling tolerance."""
        self.assertAlmostEqual(parse_weight_to_lbs("70 killograms"), 154.32, places=2)
        self.assertEqual(parse_weight_to_lbs("150 pount"), 150.0)
        # Natural language removal
        self.assertEqual(parse_weight_to_lbs("weighs about 150 lbs"), 150.0)

    def test_weight_international(self):
        """Validates Asian and Latin units."""
        # 100 Jin = ~110.23 lbs
        self.assertAlmostEqual(parse_weight_to_lbs("100 jin"), 110.23, places=2)
        # 2 Arroba = ~50.7 lbs
        self.assertAlmostEqual(parse_weight_to_lbs("2 arroba"), 50.71, places=2)

    # --- HEIGHT GAUNTLET ---

    def test_height_decimal_trap(self):
        """
        CRITICAL: Ensures 5.5 ft is parsed as 5' 6" (Mathematical),
        NOT 5' 5" (Visual).
        """
        # 5.5 ft -> 5 feet + 0.5 feet (6 inches)
        self.assertEqual(parse_height_to_us("5.5 ft"), (5, 6.0))
        
        # 5.1 ft -> 5 feet + 0.1 feet (1.2 inches)
        ft, ins = parse_height_to_us("5.1 ft")
        self.assertEqual(ft, 5)
        self.assertAlmostEqual(ins, 1.2, places=2)

    def test_height_composites(self):
        """Ensures 'Visual' notation overrides decimal logic."""
        # 5' 11" -> 5 feet, 11 inches
        self.assertEqual(parse_height_to_us("5'11"), (5, 11.0))
        self.assertEqual(parse_height_to_us("5ft 11in"), (5, 11.0))

    def test_height_inference(self):
        """Ensures raw numbers are guessed correctly based on human physiology."""
        # 180 -> Too big for feet, must be CM
        ft, ins = parse_height_to_us("180")
        self.assertEqual(ft, 5) # 180cm is ~5' 11"
        
        # 1.8 -> Too small for feet, must be Meters
        ft, ins = parse_height_to_us("1.8")
        self.assertEqual(ft, 5)

if __name__ == "__main__":
    print("Running Clinical Data Edge Cases...")
    unittest.main(verbosity=2)
