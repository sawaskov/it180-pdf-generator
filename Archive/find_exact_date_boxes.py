import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
page = pdf_document[0]
drawings = page.get_drawings()

print("All boxes in Y range 520-580 (where date fields should be):")
print("=" * 80)

date_area_boxes = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for boxes in date area
        if 520 < center_y < 580 and 8 < width < 20 and 8 < height < 20:
            date_area_boxes.append({
                'center_x': center_x,
                'center_y': center_y,
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1
            })

# Sort by Y, then X
date_area_boxes.sort(key=lambda b: (b['center_y'], b['center_x']))

# Group by Y (within 2 points)
current_y = None
current_row = []
rows = []

for box in date_area_boxes:
    if current_y is None or abs(box['center_y'] - current_y) < 2:
        current_row.append(box)
        current_y = box['center_y']
    else:
        if current_row:
            rows.append(current_row)
        current_row = [box]
        current_y = box['center_y']

if current_row:
    rows.append(current_row)

for i, row in enumerate(rows):
    avg_y = sum(b['center_y'] for b in row) / len(row)
    print(f"\nRow {i+1}: Y={avg_y:.1f}, {len(row)} boxes")
    print(f"  X positions: {[f'{b['center_x']:.1f}' for b in row]}")
    if len(row) >= 8:
        print(f"  CCYY (1-4): {[f'{b['center_x']:.1f}' for b in row[:4]]}")
        print(f"  MM (5-6): {[f'{b['center_x']:.1f}' for b in row[4:6]]}")
        print(f"  DD (7-8): {[f'{b['center_x']:.1f}' for b in row[6:8]]}")

pdf_document.close()
