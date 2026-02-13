import fitz  # PyMuPDF

# Open the PDF
pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the first page
page = pdf_document[0]

# Get all drawings (rectangles/boxes)
drawings = page.get_drawings()

print("Looking for date boxes...")
print("=" * 80)

# Look for date boxes in two areas:
# Start date: around y=525-550
# End date: around y=548-575

print("\n1. START DATE boxes (around y=500-560):")
start_boxes = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for boxes around start date area
        if 500 < center_y < 560 and 8 < width < 20 and 8 < height < 20:
            start_boxes.append({
                'center_x': center_x,
                'center_y': center_y,
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
                'width': width,
                'height': height
            })

start_boxes.sort(key=lambda b: b['center_x'])

print(f"Found {len(start_boxes)} boxes for START date:")
for i, box in enumerate(start_boxes):
    print(f"  Box {i+1}: center_x={box['center_x']:.1f}, center_y={box['center_y']:.1f}")

if start_boxes:
    print(f"\n  First 4 boxes (CCYY): {[f'{b['center_x']:.1f}' for b in start_boxes[:4]]}")
    print(f"  Next 2 boxes (MM): {[f'{b['center_x']:.1f}' for b in start_boxes[4:6]]}")
    print(f"  Last 2 boxes (DD): {[f'{b['center_x']:.1f}' for b in start_boxes[6:8]]}")
    avg_y = sum(box['center_y'] for box in start_boxes) / len(start_boxes)
    print(f"  Y center: {avg_y:.1f}")

print("\n2. END DATE boxes (around y=560-620):")
end_boxes = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for boxes around end date area
        if 560 < center_y < 620 and 8 < width < 20 and 8 < height < 20:
            end_boxes.append({
                'center_x': center_x,
                'center_y': center_y,
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
                'width': width,
                'height': height
            })

end_boxes.sort(key=lambda b: b['center_x'])

print(f"Found {len(end_boxes)} boxes for END date:")
for i, box in enumerate(end_boxes):
    print(f"  Box {i+1}: center_x={box['center_x']:.1f}, center_y={box['center_y']:.1f}")

if end_boxes:
    print(f"\n  First 4 boxes (CCYY): {[f'{b['center_x']:.1f}' for b in end_boxes[:4]]}")
    print(f"  Next 2 boxes (MM): {[f'{b['center_x']:.1f}' for b in end_boxes[4:6]]}")
    print(f"  Last 2 boxes (DD): {[f'{b['center_x']:.1f}' for b in end_boxes[6:8]]}")
    avg_y = sum(box['center_y'] for box in end_boxes) / len(end_boxes)
    print(f"  Y center: {avg_y:.1f}")

pdf_document.close()
