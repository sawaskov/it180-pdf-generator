import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
page = pdf_document[1]  # Page 2

print("Page 2 - All white blocks (large rectangles):")
print("=" * 80)

drawings = page.get_drawings()

# Find large white rectangles
white_blocks = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_y = (y0 + y1) / 2

        # Look for large rectangles (likely text input fields)
        if width > 200 and 10 < height < 30:
            white_blocks.append({
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
                'center_y': center_y,
                'width': width,
                'height': height
            })

# Sort by Y position
white_blocks.sort(key=lambda b: b['center_y'])

print(f"Found {len(white_blocks)} white blocks:\n")
for i, block in enumerate(white_blocks):
    print(f"Block {i+1}:")
    print(f"  X: {block['x0']:.1f} to {block['x1']:.1f}")
    print(f"  Y: {block['y0']:.1f} to {block['y1']:.1f} (center: {block['center_y']:.1f})")
    print(f"  Size: {block['width']:.1f} x {block['height']:.1f}")
    print()

# Also check for text labels nearby
print("\nText labels on page 2 containing 'name' or 'Name' or 'Representative':")
print("=" * 80)
text_dict = page.get_text("dict")
for block in text_dict["blocks"]:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                if "name" in text.lower() or "representative" in text.lower():
                    bbox = span["bbox"]
                    print(f"'{text}' at Y={bbox[1]:.1f}-{bbox[3]:.1f}")

pdf_document.close()
