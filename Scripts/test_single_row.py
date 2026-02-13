"""Test script to verify setup with just one row"""
import os
import sys

# Get the parent directory (SARS Pdf folder)
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Add Scripts folder to path
sys.path.insert(0, script_dir)

# Import the main functions
from fill_pdf_complete import populate_pdf_for_row
import pandas as pd

# Define paths
input_file = os.path.join(parent_dir, 'Input', 'PEG 12H allowance - FY2025 (Clean).xlsx')
output_dir = os.path.join(parent_dir, 'Output', 'Test')
template_file = os.path.join(parent_dir, 'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Create test output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Testing IT180 PDF Generator Setup")
print("=" * 80)
print(f"Input file: {input_file}")
print(f"Template: {template_file}")
print(f"Output: {output_dir}")
print()

# Check files exist
if not os.path.exists(input_file):
    print(f"ERROR: Input file not found!")
    sys.exit(1)

if not os.path.exists(template_file):
    print(f"ERROR: Template file not found!")
    sys.exit(1)

print("[OK] Input file found")
print("[OK] Template file found")
print()

# Read first row
df = pd.read_excel(input_file)
print(f"Excel file loaded: {len(df)} rows")
print()

# Process first row only
print("Processing first row as test...")
row = df.iloc[0]
output_file = populate_pdf_for_row(row, 1, template_file)

# Move to test folder
import shutil
dest_path = os.path.join(output_dir, output_file)
if os.path.exists(output_file):
    shutil.move(output_file, dest_path)
    print(f"[OK] Test PDF created successfully!")
    print(f"  Location: {dest_path}")
    print()
    print("Setup is working correctly!")
else:
    print("ERROR: PDF was not created")
    sys.exit(1)
