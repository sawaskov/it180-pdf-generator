import fitz  # PyMuPDF

# Open the PDF
pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

# Get the first page
page = pdf_document[0]

# Get all drawings (rectangles/boxes)
drawings = page.get_drawings()

print("Looking for SDL Reference boxes (around y=326-345 area)...")
print("=" * 80)

# Filter for small boxes around the SDL reference area (y around 326-345)
sdl_boxes = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        height = y1 - y0
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2

        # Look for small boxes around y=326-345 area (SDL reference line)
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
for i, box in enumerate(sdl_boxes):
    print(f"Box {i+1}: center_x={box['center_x']:.1f}, center_y={box['center_y']:.1f}, size={box['width']:.1f}x{box['height']:.1f}")

print("\n" + "=" * 80)
print("\nX positions for code:")
x_positions = [f"{box['center_x']:.1f}" for box in sdl_boxes]
print(f"boxes_x = [{', '.join(x_positions)}]")

if sdl_boxes:
    avg_y = sum(box['center_y'] for box in sdl_boxes) / len(sdl_boxes)
    print(f"y_pos = convert_y({avg_y:.1f})")

pdf_document.close()
