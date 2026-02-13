import fitz  # PyMuPDF

# Open the PDF
pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the first page
page = pdf_document[0]

# Get all drawings (rectangles/boxes)
drawings = page.get_drawings()

print("SDL Reference boxes (detailed info):")
print("=" * 80)

# Filter for boxes around the SDL reference area
sdl_boxes = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for boxes around y=326-345 area (SDL reference line)
        if 320 < center_y < 350 and 8 < width < 20 and 8 < height < 20:
            sdl_boxes.append({
                'center_x': center_x,
                'center_y': center_y,
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
                'width': width,
                'height': height
            })

# Sort by x position
sdl_boxes.sort(key=lambda b: b['center_x'])

print(f"Found {len(sdl_boxes)} boxes for SDL reference:")
print()
for i, box in enumerate(sdl_boxes):
    print(f"Box {i+1}:")
    print(f"  X: {box['x0']:.1f} to {box['x1']:.1f} (center: {box['center_x']:.1f})")
    print(f"  Y: {box['y0']:.1f} to {box['y1']:.1f} (center: {box['center_y']:.1f})")
    print(f"  Size: {box['width']:.1f} x {box['height']:.1f}")
    print()

print("=" * 80)
print("\nFor boxes 2-10 (skipping first box with L):")
boxes_2_to_10 = sdl_boxes[1:10]
x_positions = [f"{box['center_x']:.1f}" for box in boxes_2_to_10]
print(f"boxes_x = [{', '.join(x_positions)}]")

if boxes_2_to_10:
    avg_y = sum(box['center_y'] for box in boxes_2_to_10) / len(boxes_2_to_10)
    print(f"y_center = {avg_y:.1f}")
    print(f"y_pos = convert_y({avg_y:.1f})")

pdf_document.close()
