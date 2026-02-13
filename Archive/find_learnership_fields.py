import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
page = pdf_document[0]

# Find the "Particulars of title and code" label
text_dict = page.get_text("dict")

print("Looking for 'Particulars of title' label:")
print("=" * 80)

for block in text_dict["blocks"]:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                if "Particulars of title" in text or "title and code" in text:
                    bbox = span["bbox"]
                    print(f"Text: '{text}'")
                    print(f"  Position: Y={bbox[1]:.1f}-{bbox[3]:.1f}")

# Now find white rectangles below that label (around y=400-470 based on previous findings)
print("\n\nLooking for white rectangles around y=400-480:")
print("=" * 80)

drawings = page.get_drawings()

# Look for large white/light rectangles in the learnership area
rects = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_y = (y0 + y1) / 2

        # Look for medium-sized rectangles in the learnership area
        if 400 < center_y < 480 and width > 200 and 15 < height < 30:
            rects.append({
                'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
                'center_x': (x0 + x1) / 2,
                'center_y': center_y,
                'width': width,
                'height': height
            })

# Sort by Y position
rects.sort(key=lambda r: r['center_y'])

print(f"Found {len(rects)} white rectangles:\n")
for i, rect in enumerate(rects):
    print(f"Rectangle {i+1}:")
    print(f"  X: {rect['x0']:.1f} to {rect['x1']:.1f} (center: {rect['center_x']:.1f})")
    print(f"  Y: {rect['y0']:.1f} to {rect['y1']:.1f} (center: {rect['center_y']:.1f})")
    print(f"  Size: {rect['width']:.1f} x {rect['height']:.1f}")
    print()

pdf_document.close()
