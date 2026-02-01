"""
make-run.py: Clinical Data Normalizer CLI.

A robust command-line interface that allows users to input raw clinical data
and receive standardized outputs.

NOTE: This script uses importlib to dynamically load libraries because
filenames with hyphens (e.g., weight-normalizer.py) cannot be imported normally.
"""

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

# Load the logic libraries
weight_lib = load_library("weight_normalizer", "weight-normalizer.py")
height_lib = load_library("height_normalizer", "height-normalizer.py")

# Create easy aliases
parse_weight = weight_lib.parse_weight_to_lbs
parse_height = height_lib.parse_height_to_us
format_height = height_lib.format_height

# --- INTERACTIVE INTERFACE ---

def get_valid_input(prompt, parser_func, formatter=None):
    """Loops until the user provides valid input or quits."""
    while True:
        data = input(f"\n{prompt}").strip()
        
        if data.lower() in ['q', 'quit', 'exit']:
            print("Exiting...")
            sys.exit(0)
            
        try:
            result = parser_func(data)
            if formatter:
                return formatter(*result)
            return result
        except ValueError as e:
            print(f"   [Error] {e}")
            print("   Please try again.")

def main():
    print("="*60)
    print("      CLINICAL DATA NORMALIZER (Interactive Mode)")
    print("      Type 'q' to quit at any time.")
    print("="*60)

    while True:
        # 1. Process Weight
        w_lbs = get_valid_input(
            "Enter Weight (e.g., 70kg, 11st 6, 150 lbs): ", 
            parse_weight
        )

        # 2. Process Height
        h_str = get_valid_input(
            "Enter Height (e.g., 180cm, 5'11, 1.8m): ", 
            parse_height, 
            format_height
        )

        # 3. Display Report
        print("\n" + "*"*40)
        print("          STANDARDIZED REPORT")
        print("*"*40)
        print(f"  WEIGHT: {w_lbs:.2f} lbs")
        print(f"  HEIGHT: {h_str}")
        print("*"*40)
        
        # 4. Loop or Quit
        again = input("\nProcess another patient? (y/n): ")
        if again.lower() != 'y':
            print("Goodbye.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
