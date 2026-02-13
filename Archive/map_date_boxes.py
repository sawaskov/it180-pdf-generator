import fitz  # PyMuPDF

pdf_document = fitz.open('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
page = pdf_document[0]
drawings = page.get_drawings()

# Find vertical lines in date areas to determine box boundaries
print("Mapping date box structure:")
print("=" * 80)

# Get vertical lines (width=0) in date areas
start_date_y = 532.1
end_date_y = 562.7

vertical_lines = []
for drawing in drawings:
    rect = drawing.get("rect", None)
    if rect:
        x0, y0, x1, y1 = rect
        width = x1 - x0
        center_y = (y0 + y1) / 2

        # Find vertical separators in start date row
        if abs(center_y - start_date_y) < 2 and width == 0.0:
            vertical_lines.append(x0)

vertical_lines = sorted(set(vertical_lines))

print(f"\nStart Date (Y={start_date_y}):")
print(f"Vertical lines at X: {[f'{x:.1f}' for x in vertical_lines]}")

# The boxes are between these lines
# Format: CCYY | MM | DD
# Let's identify the groups based on the larger boxes we saw
print("\nBased on the rectangles found:")
print("  CCYY box: X=440.2 to 488.1 (4 digits)")
print("  MM box: X=500.6 to 524.6 (2 digits)")
print("  DD box: X=536.8 to 560.8 (2 digits)")

# Calculate individual digit positions
# CCYY: 4 digits in space from 440.2 to 488.1 (width 47.9)
ccyy_start = 440.2
ccyy_width = 47.9
digit_width = ccyy_width / 4
ccyy_positions = [ccyy_start + (i * digit_width) + (digit_width / 2) for i in range(4)]

# MM: 2 digits in space from 500.6 to 524.6 (width 24.0)
mm_start = 500.6
mm_width = 24.0
mm_digit_width = mm_width / 2
mm_positions = [mm_start + (i * mm_digit_width) + (mm_digit_width / 2) for i in range(2)]

# DD: 2 digits in space from 536.8 to 560.8 (width 24.0)
dd_start = 536.8
dd_width = 24.0
dd_digit_width = dd_width / 2
dd_positions = [dd_start + (i * dd_digit_width) + (dd_digit_width / 2) for i in range(2)]

print("\nCalculated center positions for digits:")
print(f"  CCYY: {[f'{x:.1f}' for x in ccyy_positions]}")
print(f"  MM: {[f'{x:.1f}' for x in mm_positions]}")
print(f"  DD: {[f'{x:.1f}' for x in dd_positions]}")

print(f"\nStart date Y: {start_date_y}")
print(f"End date Y: {end_date_y}")

pdf_document.close()
