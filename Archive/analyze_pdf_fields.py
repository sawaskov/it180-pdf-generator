import fitz  # PyMuPDF
import pandas as pd

# Open the PDF
pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the first page
page = pdf_document[0]

# Get page dimensions
print(f"Page dimensions: {page.rect.width} x {page.rect.height}")
print(f"Page size: {page.rect}")

# Extract text with positions
text_instances = page.get_text("dict")

print("\n\nKey text positions on the form:")
print("=" * 80)

# Look for key labels to find their positions
for block in text_instances["blocks"]:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].strip()
                if any(keyword in text for keyword in [
                    "Income Tax Reference",
                    "Year of Assessment",
                    "Registered name of employer",
                    "Skills Development Levy",
                    "Name of SETA",
                    "Particulars of title",
                    "Full names and identity",
                    "Date of entering",
                    "Date of completion",
                    "Was the learner",
                    "Period of",
                    "annual equivalent",
                    "amount of the deduction",
                    "limitation"
                ]):
                    bbox = span["bbox"]
                    print(f"Text: '{text[:50]}'")
                    print(f"  Position: x={bbox[0]:.1f}, y={bbox[1]:.1f} to x={bbox[2]:.1f}, y={bbox[3]:.1f}")
                    print()

pdf_document.close()

print("\nNote: In PDFs, Y coordinates start from TOP of page")
print("To position text correctly, I need to place it slightly BELOW the label text")
