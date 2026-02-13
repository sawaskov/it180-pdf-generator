import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

print(f"PDF has {len(pdf_document)} pages")
print("=" * 80)

# Get the last page
page = pdf_document[-1]

print(f"\nPage {len(pdf_document)} dimensions: {page.rect.width} x {page.rect.height}")

# Get all drawings
drawings = page.get_drawings()

# Look for boxes on the right side, bottom area
print("\n\nLooking for date boxes on bottom right of last page:")
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

        # Look for boxes on bottom half, right side
        if center_y > 400 and center_x > 300 and 8 < width < 20 and 8 < height < 20:
            found_row = False
            for row_y in rows.keys():
                if abs(center_y - row_y) < 5:
                    rows[row_y].append({'center_x': center_x, 'center_y': center_y, 'width': width, 'height': height})
                    found_row = True
                    break
            if not found_row:
                rows[center_y] = [{'center_x': center_x, 'center_y': center_y, 'width': width, 'height': height}]

# Sort rows by Y position
sorted_rows = sorted(rows.items(), key=lambda x: x[0])

print(f"Found {len(sorted_rows)} rows of boxes on bottom right:\n")
for row_y, boxes in sorted_rows:
    boxes.sort(key=lambda b: b['center_x'])
    print(f"Y={row_y:.1f}: {len(boxes)} boxes")
    if len(boxes) >= 8:  # Could be a date row (CCYYMMDD)
        print(f"  X positions: {[f'{b['center_x']:.1f}' for b in boxes[:8]]}")
        print(f"  First 4 (CCYY): {[f'{b['center_x']:.1f}' for b in boxes[:4]]}")
        print(f"  Next 2 (MM): {[f'{b['center_x']:.1f}' for b in boxes[4:6]]}")
        print(f"  Last 2 (DD): {[f'{b['center_x']:.1f}' for b in boxes[6:8]]}")

pdf_document.close()
