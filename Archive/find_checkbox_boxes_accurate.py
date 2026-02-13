import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Check both pages for checkbox boxes
for page_num in [0, 1]:
    page = pdf_document[page_num]
    drawings = page.get_drawings()

    print(f"\n{'='*80}")
    print(f"PAGE {page_num + 1} - All small boxes on right side:")
    print('='*80)

    # Find all small square boxes
    boxes = []
    for drawing in drawings:
        rect = drawing.get("rect", None)
        if rect:
            x0, y0, x1, y1 = rect
            width = x1 - x0
            height = y1 - y0
            center_x = (x0 + x1) / 2
            center_y = (y0 + y1) / 2

            # Look for small boxes on right side (likely checkboxes)
            if center_x > 480 and 10 < width < 25 and 10 < height < 25:
                boxes.append({
                    'center_x': center_x,
                    'center_y': center_y,
                    'x0': x0,
                    'y0': y0,
                    'x1': x1,
                    'y1': y1,
                    'width': width,
                    'height': height
                })

    # Sort by Y position
    boxes.sort(key=lambda b: b['center_y'])

    print(f"Found {len(boxes)} checkbox-sized boxes:\n")

    # Group by Y position (within 5 points)
    current_y = None
    current_row = []
    rows = []

    for box in boxes:
        if current_y is None or abs(box['center_y'] - current_y) < 5:
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
        row.sort(key=lambda b: b['center_x'])
        avg_y = sum(b['center_y'] for b in row) / len(row)
        print(f"Row {i+1} at Y={avg_y:.1f}: {len(row)} boxes")
        for j, box in enumerate(row):
            print(f"  Box {j+1}: center_x={box['center_x']:.1f}, center_y={box['center_y']:.1f}")
            print(f"    Bounds: X={box['x0']:.1f}-{box['x1']:.1f}, Y={box['y0']:.1f}-{box['y1']:.1f}")
            print(f"    Size: {box['width']:.1f} x {box['height']:.1f}")

pdf_document.close()
