import pandas as pd
from pypdf import PdfReader, PdfWriter
import sys

# Read Excel file
df = pd.read_excel('PEG 12H allowance - FY2025 (2).xlsx')

# Get first row
row = df.iloc[0]

# Read the PDF
reader = PdfReader('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
writer = PdfWriter()

# Copy all pages
for page in reader.pages:
    writer.add_page(page)

# Get form fields to see what's available
print("Available form fields:")
if reader.get_fields():
    for field_name in reader.get_fields().keys():
        print(f"  - {field_name}")
else:
    print("  No fillable fields found in PDF")

# Map Excel columns to PDF form fields
field_mapping = {
    'Inkomstebelastingverwysingsnommer van werkgewer': str(row['Inkomstebelastingverwysingsnommer van werkgewer']) if pd.notna(row['Inkomstebelastingverwysingsnommer van werkgewer']) else '',
    'Year of Assessment': str(int(row['Year of Assessment'])) if pd.notna(row['Year of Assessment']) else '',
    'Geregistreerde naam van werkgewer': str(row['Geregistreerde naam van werkgewer']) if pd.notna(row['Geregistreerde naam van werkgewer']) else '',
    'Vaardigheidsontwikkelingsheffingverwysingsnommer': str(row['Vaardigheidsontwikkelingsheffingverwysingsnommer']) if pd.notna(row['Vaardigheidsontwikkelingsheffingverwysingsnommer']) else '',
    'Naam van SETA waar die leerlingooreenkoms geregistreer is': str(row['Naam van SETA waar die leerlingooreenkoms geregistreer is']) if pd.notna(row['Naam van SETA waar die leerlingooreenkoms geregistreer is']) else '',
    'Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership': str(row['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) if pd.notna(row['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) else '',
    'Full names and identity number of the learner contemplated in the registered learnership agreement': str(row['Full names and identity number of the learner contemplated in the registered learnership agreement']) if pd.notna(row['Full names and identity number of the learner contemplated in the registered learnership agreement']) else '',
    'Start date': str(row['Start date']) if pd.notna(row['Start date']) else '',
    'End date': str(row['End date']) if pd.notna(row['End date']) else '',
}

# Print data being filled
print("\n\nData from Excel row 1:")
for key, value in field_mapping.items():
    print(f"{key}: {value}")

# Try to fill the form if fields exist
if reader.get_fields():
    writer.update_page_form_field_values(
        writer.pages[0], field_mapping
    )
    print("\n✓ Form fields populated")
else:
    print("\n⚠ Warning: PDF has no fillable form fields. The PDF may need to be filled manually or converted to a fillable form.")

# Save the output
output_filename = f'IT180_Row1_{row["Full names and identity number of the learner contemplated in the registered learnership agreement"].replace(" ", "_")}.pdf'
with open(output_filename, 'wb') as output_file:
    writer.write(output_file)

print(f"\n✓ PDF saved as: {output_filename}")
