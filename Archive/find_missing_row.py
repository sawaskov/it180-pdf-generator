import pandas as pd
import os

# Read the Excel file
df = pd.read_excel('PEG 12H allowance - FY2025 (Clean).xlsx')

# Get list of generated PDF files
output_dir = 'IT180 Docs'
generated_files = os.listdir(output_dir)
generated_files = [f for f in generated_files if f.endswith('.pdf')]

print(f"Total rows in Excel: {len(df)}")
print(f"Total PDFs generated: {len(generated_files)}")
print()

# Check which learner names have PDFs
missing_rows = []

for index, row in df.iterrows():
    learner_name = str(row['Full Names']) if pd.notna(row['Full Names']) else ''
    safe_name = learner_name.replace(" ", "_") if learner_name else "Unknown"
    expected_filename = f'IT180_{safe_name}.pdf'

    if expected_filename not in generated_files:
        missing_rows.append({
            'row': index + 1,
            'learner_name': learner_name,
            'expected_filename': expected_filename
        })

if missing_rows:
    print(f"Found {len(missing_rows)} missing PDF(s):")
    print("=" * 80)
    for missing in missing_rows:
        print(f"Row {missing['row']}: {missing['learner_name']}")
        print(f"  Expected filename: {missing['expected_filename']}")
        print()
else:
    print("All PDFs generated successfully!")

# Also check for duplicate names
from collections import Counter
learner_names = []
for index, row in df.iterrows():
    learner_name = str(row['Full Names']) if pd.notna(row['Full Names']) else ''
    learner_names.append(learner_name)

duplicates = [name for name, count in Counter(learner_names).items() if count > 1]

if duplicates:
    print("\nNote: Found duplicate learner names (may have overwritten PDFs):")
    print("=" * 80)
    for dup_name in duplicates:
        dup_rows = [i+1 for i, name in enumerate(learner_names) if name == dup_name]
        print(f"{dup_name}: Rows {dup_rows}")
