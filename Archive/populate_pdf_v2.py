import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Read Excel file
df = pd.read_excel('PEG 12H allowance - FY2025 (2).xlsx')

# Get first row
row = df.iloc[0]

print("Data from Excel row 1:")
print(f"Tax Reference Number: {row['Inkomstebelastingverwysingsnommer van werkgewer']}")
print(f"Year of Assessment: {int(row['Year of Assessment'])}")
print(f"Employer Name: {row['Geregistreerde naam van werkgewer']}")
print(f"SDL Reference: {row['Skills Development Levy reference number']}")
print(f"SETA Name: {row['Naam van SETA waar die leerlingooreenkoms geregistreer is']}")
print(f"Learnership Title: {row['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']}")
print(f"Learner Name & ID: {row['Full names and identity number of the learner contemplated in the registered learnership agreement']}")
print(f"Start Date: {row['Start date']}")
print(f"End Date: {row['End date']}")
print(f"Was Employed: {row['Was the learner at the time of entering into the learnership agreement employed']}")
print(f"Was Disabled: {row['Was the learner at the time of entering into the learnership agreement, a disabled person?']}")
print(f"In course of trade: {row['Was the learnership agreement entered into between the employer and the learner in the course of any trade carried on by that employer?']}")
print(f"Annual Remuneration: {row['The annual equivalent or the total remuneration as stipulated in the employment']}")
print(f"Deduction Claimed: {row['Rands only_2']}")
print(f"Limitation: {row['Rands only_3']}")

print("\n\nThe PDF does not have fillable form fields.")
print("To populate this PDF, we need to:")
print("1. Create an overlay PDF with text at specific coordinates")
print("2. Merge it with the original PDF")
print("\nWould you like me to create a solution that overlays the data onto the PDF at the correct positions?")
print("This will require identifying the coordinates for each field on the PDF form.")
