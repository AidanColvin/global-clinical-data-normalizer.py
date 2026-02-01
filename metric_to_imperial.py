"""
Metric to Imperial Unit Converter.

This module provides utilities to convert standardized medical metrics (Mass in Kg, 
Height in Cm) into US Imperial units (Lbs/Oz, Ft/In). 
It is designed for use in clinical data pipelines where patient-facing displays require localization.

Typical usage example:

  result = convert_health_metrics(weight_kg=70.5, height_cm=178.0)
  print(result)
"""

from typing import Dict, Union

def convert_health_metrics(weight_kg: float, height_cm: float) -> Dict[str, Union[int, float]]:
    """Converts metric health measurements to imperial units.

    Calculates weight in pounds/ounces and height in feet/inches using standard
    conversion factors. 

    Args:
        weight_kg: A float representing the patient's mass in Kilograms.
        height_cm: A float representing the patient's height in Centimeters.

    Returns:
        A dictionary containing the converted values with the following keys:
        - 'weight_lbs': (int) The pound component of weight.
        - 'weight_oz': (float) The remaining ounce component (rounded to 1 decimal).
        - 'height_ft': (int) The feet component of height.
        - 'height_in': (float) The remaining inch component (rounded to 1 decimal).

    Raises:
        ValueError: If inputs are negative.
    """
    
    # Validate inputs to ensure physical possibility
    if weight_kg < 0 or height_cm < 0:
        raise ValueError("Weight and height must be non-negative values.")

    # --- WEIGHT CONVERSION ---
    # Constant: 1 Kilogram = 2.20462 Pounds
    CONVERSION_KG_TO_LBS = 2.20462
    total_lbs = weight_kg * CONVERSION_KG_TO_LBS
    
    pounds = int(total_lbs)
    # The fractional remainder is converted to ounces (1 lb = 16 oz)
    ounces = (total_lbs - pounds) * 16
    
    # --- HEIGHT CONVERSION ---
    # Constant: 1 Inch = 2.54 Centimeters
    CONVERSION_INCH_TO_CM = 2.54
    total_inches = height_cm / CONVERSION_INCH_TO_CM
    
    feet = int(total_inches // 12)  # Floor division to get whole feet
    inches = total_inches % 12      # Modulo to get remaining inches
    
    return {
        "weight_lbs": pounds,
        "weight_oz": round(ounces, 1),
        "height_ft": feet,
        "height_in": round(inches, 1)
    }

def main() -> None:
    """Main execution function handling user Input/Output."""
    print("--- Clinical Unit Converter (Metric -> Imperial) ---")
    print("Type '0' at any prompt to exit the program.\n")
    
    while True:
        try:
            # Type casting inputs immediately to float for calculation
            kg_input_str = input("Enter Patient Weight (kg): ")
            kg_input = float(kg_input_str)
            if kg_input == 0:
                print("Exiting program.")
                break
            
            cm_input_str = input("Enter Patient Height (cm): ")
            cm_input = float(cm_input_str)
            
            # Execute conversion logic
            results = convert_health_metrics(weight_kg=kg_input, height_cm=cm_input)
            
            # Display results using f-strings for clean formatting
            print("-" * 30)
            print(f"Weight: {results['weight_lbs']} lbs  {results['weight_oz']} oz")
            print(f"Height: {results['height_ft']} ft   {results['height_in']} in")
            print("-" * 30 + "\n")
            
        except ValueError:
            # Handles non-numeric inputs (e.g., users typing "seventy")
            print("\n[!] Error: Invalid input. Please enter numeric values only (e.g., 70.5).\n")

if __name__ == "__main__":
    main()
