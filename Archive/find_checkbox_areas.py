import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Check both pages for checkbox areas
for page_num in [0, 1]:
    page = pdf_document[page_num]
    drawings = page.get_drawings()

    print(f"\n{'='*80}")
    print(f"PAGE {page_num + 1} - White rectangles on right side (checkbox areas):")
    print('='*80)

    # Find rectangles that are likely checkbox containers
    if page_num == 0:
        y_ranges = [(590, 605), (615, 630), (640, 660)]
    else:
        y_ranges = [(55, 75), (95, 115), (155, 175)]

    for i, (y_min, y_max) in enumerate(y_ranges):
        print(f"\nCheckbox area {i+1} (Y={y_min}-{y_max}):")
        rects = []
        for drawing in drawings:
            rect = drawing.get("rect", None)
            if rect:
                x0, y0, x1, y1 = rect
                width = x1 - x0
                height = y1 - y0
                center_x = (x0 + x1) / 2
                center_y = (y0 + y1) / 2

                # Look for rectangles in the checkbox Y range
                if y_min < center_y < y_max and center_x > 400:
                    rects.append({
                        'center_x': center_x,
                        'center_y': center_y,
                        'x0': x0,
                        'y0': y0,
                        'x1': x1,
                        'y1': y1,
                        'width': width,
                        'height': height
                    })

        rects.sort(key=lambda r: r['center_x'])

        for j, rect in enumerate(rects):
            print(f"  Rectangle {j+1}:")
            print(f"    X: {rect['x0']:.1f}-{rect['x1']:.1f} (center: {rect['center_x']:.1f})")
            print(f"    Y: {rect['y0']:.1f}-{rect['y1']:.1f} (center: {rect['center_y']:.1f})")
            print(f"    Size: {rect['width']:.1f} x {rect['height']:.1f}")

pdf_document.close()
