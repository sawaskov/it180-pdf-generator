import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the last page
page = pdf_document[-1]

print(f"Page 2 - Looking for all rectangles on bottom half (Y > 400):")
print("=" * 80)

# Get all drawings
drawings = page.get_drawings()

# Look for all rectangles on bottom half
rectangles = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for rectangles on bottom half
        if center_y > 600:  # Focus on bottom area
            rectangles.append({
                'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
                'center_x': center_x, 'center_y': center_y,
                'width': width, 'height': height
            })

# Sort by Y position
rectangles.sort(key=lambda r: (r['center_y'], r['center_x']))

print(f"Found {len(rectangles)} rectangles on bottom area:\n")

# Group by similar Y positions
current_y = None
current_group = []
groups = []

for rect in rectangles:
    if current_y is None or abs(rect['center_y'] - current_y) < 5:
        current_group.append(rect)
        current_y = rect['center_y']
    else:
        if current_group:
            groups.append(current_group)
        current_group = [rect]
        current_y = rect['center_y']

if current_group:
    groups.append(current_group)

for i, group in enumerate(groups):
    avg_y = sum(r['center_y'] for r in group) / len(group)
    print(f"\nGroup at Y={avg_y:.1f}: {len(group)} rectangles")
    for rect in group:
        print(f"  X={rect['x0']:.1f}-{rect['x1']:.1f}, Y={rect['y0']:.1f}-{rect['y1']:.1f}, size={rect['width']:.1f}x{rect['height']:.1f}")

# Also look for text mentions of "Date"
print("\n\nText containing 'Date' on page 2:")
print("=" * 80)
text_dict = page.get_text("dict")
for block in text_dict["blocks"]:
    if "lines" in block:
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"]
                if "Date" in text or "date" in text:
                    bbox = span["bbox"]
                    print(f"'{text}' at Y={bbox[1]:.1f}-{bbox[3]:.1f}, X={bbox[0]:.1f}-{bbox[2]:.1f}")

pdf_document.close()
