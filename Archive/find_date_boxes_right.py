import fitz  # PyMuPDF

# Open the PDF
pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the first page
page = pdf_document[0]

# Get all drawings (rectangles/boxes)
drawings = page.get_drawings()

print("Looking for date boxes on RIGHT side of page (x > 400):")
print("=" * 80)

# Group boxes by Y position
rows = {}
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for small boxes on right side
        if center_x > 400 and 8 < width < 20 and 8 < height < 20:
            found_row = False
            for row_y in rows.keys():
                if abs(center_y - row_y) < 5:
                    rows[row_y].append({'center_x': center_x, 'center_y': center_y})
                    found_row = True
                    break
            if not found_row:
                rows[center_y] = [{'center_x': center_x, 'center_y': center_y}]

# Sort rows by Y position
sorted_rows = sorted(rows.items(), key=lambda x: x[0])

print(f"Found {len(sorted_rows)} rows of boxes on right side:\n")
for row_y, boxes in sorted_rows:
    boxes.sort(key=lambda b: b['center_x'])
    if 500 < row_y < 600 and len(boxes) >= 8:  # Date boxes should have 8 boxes (CCYYMMDD)
        print(f"Y={row_y:.1f}: {len(boxes)} boxes")
        print(f"  First 4 (CCYY): {[f'{b['center_x']:.1f}' for b in boxes[:4]]}")
        print(f"  Next 2 (MM): {[f'{b['center_x']:.1f}' for b in boxes[4:6]]}")
        print(f"  Last 2 (DD): {[f'{b['center_x']:.1f}' for b in boxes[6:8]]}")
        print()

pdf_document.close()
