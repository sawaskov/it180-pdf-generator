import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
page = pdf_document[0]

print("All rectangles in Y range 410-470:")
print("=" * 80)

drawings = page.get_drawings()

rects = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_y = (y0 + y1) / 2

        # Look for ANY rectangles in the learnership area
        if 410 < center_y < 470:
            rects.append({
                'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1,
                'center_x': (x0 + x1) / 2,
                'center_y': center_y,
                'width': width,
                'height': height
            })

# Sort by Y position
rects.sort(key=lambda r: r['center_y'])

print(f"Found {len(rects)} rectangles:\n")
for i, rect in enumerate(rects):
    print(f"Rectangle {i+1}:")
    print(f"  X: {rect['x0']:.1f} to {rect['x1']:.1f}")
    print(f"  Y: {rect['y0']:.1f} to {rect['y1']:.1f} (center: {rect['center_y']:.1f})")
    print(f"  Size: {rect['width']:.1f} x {rect['height']:.1f}")
    print()

# Also check existing white block centers we found earlier
print("\nPreviously found white block centers:")
print("  Y=296.7, 312.6, 373.0, 388.9, 443.0, 458.9, 494.7")
print("\nThe learnership fields should be around Y=443.0 and Y=458.9")

pdf_document.close()
