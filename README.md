## Health Normalizer

# Clinical Metric to Imperial Converter

## Overview
A Python utility designed to localize standardized medical data. This tool accepts metric inputs (commonly found in research databases like REDCap) and converts them into imperial units (Lbs/Oz, Ft/In) for US-based provider review or patient-facing displays.

This project demonstrates **ETL data transformation logic**, **Type Inference**, and **Test-Driven Development (TDD)** patterns.

## Features
* **Precise Weight Conversion:** Converts raw float Kg into split Pounds and Ounces.
* **Height Logic:** Transforms Cm into Feet and Inches using integer division.
* **Type Hinting:** fully typed for better code reliability and IDE support.
* **Error Handling:** Validates non-negative inputs and manages non-numeric user entry.

## Tech Stack
* **Language:** Python 3.10+
* **Libraries:** `unittest` (Standard Library) - No external dependencies required.

## Project Structure
```text
├── metric_to_imperial.py   # Main logic and user interface
├── test_converter.py       # Unit test suite
└── README.md               # Project documentation
