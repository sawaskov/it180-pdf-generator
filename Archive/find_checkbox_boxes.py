import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Check page 1 checkboxes
for page_num in [0, 1]:
    page = pdf_document[page_num]
    drawings = page.get_drawings()

    print(f"\n{'='*80}")
    print(f"PAGE {page_num + 1} - Checkbox boxes:")
    print('='*80)

    # Find small square boxes on the right side
    if page_num == 0:
        y_ranges = [(590, 605), (615, 630), (640, 660)]  # Page 1 checkbox areas
    else:
        y_ranges = [(55, 75), (95, 115), (155, 175)]  # Page 2 checkbox areas

    for i, (y_min, y_max) in enumerate(y_ranges):
        print(f"\nCheckbox row {i+1} (Y={y_min}-{y_max}):")
        boxes = []
        for drawing in drawings:
            rect = drawing.get("rect", None)
            if rect:
                x0, y0, x1, y1 = rect
                width = x1 - x0
                height = y1 - y0
                center_x = (x0 + x1) / 2
                center_y = (y0 + y1) / 2

                # Look for small squares in the Y range, right side
                if y_min < center_y < y_max and 400 < center_x < 600 and 8 < width < 20 and 8 < height < 20:
                    boxes.append({
                        'center_x': center_x,
                        'center_y': center_y,
                        'x0': x0,
                        'y0': y0,
                        'x1': x1,
                        'y1': y1
                    })

        boxes.sort(key=lambda b: b['center_x'])

        if len(boxes) >= 2:
            print(f"  YES box: center X={boxes[0]['center_x']:.1f}, Y={boxes[0]['center_y']:.1f}")
            print(f"  NO box: center X={boxes[1]['center_x']:.1f}, Y={boxes[1]['center_y']:.1f}")
        else:
            print(f"  Found {len(boxes)} boxes")

pdf_document.close()
