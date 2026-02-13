import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
page = pdf_document[0]

# Extract text to find date field labels
text_dict = page.get_text("dict")

print("Finding 'Date of entering' and 'Date of completion' labels:")
print("=" * 80)

for block in text_dict["blocks"]:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                if "Date of entering" in text or "Date of completion" in text:
                    bbox = span["bbox"]
                    print(f"\nText: '{text}'")
                    print(f"  Position: y={bbox[1]:.1f} to {bbox[3]:.1f}")

# Now check for all drawings/shapes in those areas
drawings = page.get_drawings()

print("\n\nAll rectangles in Y range 530-570:")
print("=" * 80)

for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        center_y = (y0 + y1) / 2
        if 530 < center_y < 570:
            width = x1 - x0
            height = y1 - y0
            print(f"Rectangle at Y={center_y:.1f}: X={x0:.1f}-{x1:.1f}, size={width:.1f}x{height:.1f}")

pdf_document.close()
