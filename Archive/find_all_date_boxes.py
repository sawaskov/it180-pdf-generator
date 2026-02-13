import fitz  # PyMuPDF

# Open the PDF
pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the first page
page = pdf_document[0]

# Get all drawings (rectangles/boxes)
drawings = page.get_drawings()

print("All small boxes (14x14 size) on the right side of page:")
print("=" * 80)

all_boxes = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for small boxes
        if 8 < width < 20 and 8 < height < 20:
            all_boxes.append({
                'center_x': center_x,
                'center_y': center_y,
                'width': width,
                'height': height
            })

# Group by Y position (within 5 points)
rows = {}
for box in all_boxes:
    y = box['center_y']
    found_row = False
    for row_y in rows.keys():
        if abs(y - row_y) < 5:
            rows[row_y].append(box)
            found_row = True
            break
    if not found_row:
        rows[y] = [box]

# Sort rows by Y position
sorted_rows = sorted(rows.items(), key=lambda x: x[0])

print(f"Found {len(sorted_rows)} rows of boxes:\n")
for row_y, boxes in sorted_rows:
    boxes.sort(key=lambda b: b['center_x'])
    print(f"Y={row_y:.1f}: {len(boxes)} boxes")
    if len(boxes) >= 8:  # Could be a date row
        print(f"  X positions: {[f'{b['center_x']:.1f}' for b in boxes[:8]]}")

pdf_document.close()
