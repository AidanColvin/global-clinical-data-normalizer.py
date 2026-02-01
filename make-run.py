"""
make-run.py: Clinical Data Normalizer CLI.

A robust command-line interface that allows users to input raw clinical data
and receive standardized outputs.

NOTE: Uses importlib to handle filenames with hyphens (e.g., weight-normalizer.py).
"""

import sys
import importlib.util

# --- DYNAMIC IMPORTS FOR HYPHENATED FILES ---

def load_module(module_name, file_path):
    """Helper to import files with hyphens in their names."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"Could not find file: {file_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Could not find '{file_path}'.")
        print("Ensure you are in the correct directory.")
        sys.exit(1)

# Import 'weight-normalizer.py'
weight_lib = load_module("weight_normalizer", "weight-normalizer.py")
parse_weight_to_lbs = weight_lib.parse_weight_to_lbs

# Import 'height-normalizer.py'
height_lib = load_module("height_normalizer", "height-normalizer.py")
parse_height_to_us = height_lib.parse_height_to_us
format_height = height_lib.format_height

# --------------------------------------------

def clear_screen():
    print("\n" * 2)

def get_valid_input(prompt_text, parser_func, format_func=None):
    """
    Generic retry loop. Keeps asking for input until parser_func succeeds.
    """
    while True:
        user_input = input(f"\n{prompt_text}")
        
        # Allow user to quit
        if user_input.lower() in ['q', 'quit', 'exit']:
            print("Exiting...")
            sys.exit(0)
            
        try:
            # Attempt parsing
            result = parser_func(user_input)
            
            # Optional formatting (for Height tuple -> String)
            if format_func and isinstance(result, tuple):
                return format_func(*result)
            
            return result
            
        except ValueError as e:
            print(f"   [!] Error: {e}")
            print("   Please try again (e.g., '70kg', '5ft 10').")

def main():
    print("="*60)
    print("      CLINICAL DATA NORMALIZER (Global Standard)      ")
    print("="*60)
    print("Instructions:")
    print(" - Enter any format (Metric, Imperial, Asian, Composite).")
    print(" - Type 'q' to quit at any time.")
    print("-" * 60)

    while True:
        # 1. Get Weight
        weight_lbs = get_valid_input(
            prompt_text="Enter Weight (e.g. 70kg, 11st 6, 150 lbs): ", 
            parser_func=parse_weight_to_lbs
        )

        # 2. Get Height
        height_str = get_valid_input(
            prompt_text="Enter Height (e.g. 180cm, 5'11, 1.8m): ", 
            parser_func=parse_height_to_us,
            format_func=format_height
        )

        # 3. Output Report
        print("\n" + "*"*40)
        print("          STANDARDIZED REPORT          ")
        print("*"*40)
        print(f"  WEIGHT: {weight_lbs:.2f} lbs")
        print(f"  HEIGHT: {height_str}")
        print("*"*40)
        
        # 4. Continuation Prompt
        again = input("\nProcess another patient? (y/n): ")
        if again.lower() != 'y':
            print("\nShutting down. Goodbye!")
            break
        print("\n" + "-"*40)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
