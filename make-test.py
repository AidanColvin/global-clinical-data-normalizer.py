"""
make-test.py: Unified Edge Case Test Suite.

NOTE: This script uses 'importlib' because the library filenames 
contain hyphens (weight-normalizer.py), which strictly prevents 
standard Python imports.
"""

import unittest
import sys
import importlib.util

# --- DYNAMIC IMPORT SETUP ---
def load_library(module_name, file_path):
    """Imports a Python file given its path, handling hyphenated names."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise FileNotFoundError
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        print(f"\n[CRITICAL ERROR] Could not find library file: '{file_path}'")
        print("Ensure 'weight-normalizer.py' and 'height-normalizer.py' are in this folder.")
        sys.exit(1)

# Load the libraries dynamically
weight_lib = load_library("weight_normalizer", "weight-normalizer.py")
height_lib = load_library("height_normalizer", "height-normalizer.py")

# Create aliases for easier usage inside tests
parse_weight = weight_lib.parse_weight_to_lbs
parse_height = height_lib.parse_height_to_us

# --- THE TEST SUITE ---

class TestClinicalEdgeCases(unittest.TestCase):
    
    # --- WEIGHT TESTS ---
    
    def test_weight_composites(self):
        """Validates the '11 stone 6' logic."""
        self.assertEqual(parse_weight("11st 6lb"), 160.0)
        self.assertEqual(parse_weight("11-6"), 160.0)

    def test_weight_typos(self):
        """Validates misspelling tolerance."""
        self.assertAlmostEqual(parse_weight("70 killograms"), 154.32, places=2)

    def test_weight_international(self):
        """Validates Asian and Latin units."""
        self.assertAlmostEqual(parse_weight("100 jin"), 110.23, places=2)

    # --- HEIGHT TESTS ---

    def test_height_decimal_trap(self):
        """
        CRITICAL: Ensures 5.5 ft is parsed as 5' 6" (Mathematical),
        NOT 5' 5" (Visual).
        """
        self.assertEqual(parse_height("5.5 ft"), (5, 6.0))

    def test_height_composites(self):
        """Ensures 'Visual' notation overrides decimal logic."""
        self.assertEqual(parse_height("5'11"), (5, 11.0))

    def test_height_inference(self):
        """Ensures raw numbers are guessed correctly."""
        # 180 -> CM range
        ft, ins = parse_height("180")
        self.assertEqual(ft, 5) 
        
        # 1.8 -> Meter range
        ft, ins = parse_height("1.8")
        self.assertEqual(ft, 5)

if __name__ == "__main__":
    print("Running Clinical Data Edge Cases...")
    unittest.main(verbosity=2)