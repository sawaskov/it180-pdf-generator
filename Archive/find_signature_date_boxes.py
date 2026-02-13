import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the last page
page = pdf_document[-1]

print(f"Page 2 - Looking for date boxes around Y=250-300 (where 'Date' label is):")
print("=" * 80)

# Get all drawings
drawings = page.get_drawings()

# Look for rectangles around the Date label area
date_area_rects = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for rectangles around Y=250-300
        if 250 < center_y < 310:
            date_area_rects.append({
                'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
                'center_x': center_x, 'center_y': center_y,
                'width': width, 'height': height
            })

# Sort by Y, then X
date_area_rects.sort(key=lambda r: (r['center_y'], r['center_x']))

print(f"Found {len(date_area_rects)} rectangles around Date label:\n")

# Look for grouped rectangles that form date boxes
for rect in date_area_rects:
    print(f"X={rect['x0']:.1f}-{rect['x1']:.1f} (center={rect['center_x']:.1f}), " +
          f"Y={rect['y0']:.1f}-{rect['y1']:.1f} (center={rect['center_y']:.1f}), " +
          f"size={rect['width']:.1f}x{rect['height']:.1f}")

# Look for vertical lines (separators) in that area
print("\n\nVertical lines (width=0) around date area:")
print("=" * 80)
vertical_lines = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        center_y = (y0 + y1) / 2

        if 270 < center_y < 300 and width == 0.0 and x0 > 400:  # Right side
            vertical_lines.append({'x': x0, 'y0': y0, 'y1': y1, 'center_y': center_y})

vertical_lines.sort(key=lambda v: v['x'])

for vline in vertical_lines:
    print(f"X={vline['x']:.1f}, Y={vline['y0']:.1f}-{vline['y1']:.1f}")

pdf_document.close()
