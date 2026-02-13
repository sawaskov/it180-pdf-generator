from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# Create test overlay with SDL digits
packet = io.BytesIO()
page_height = 841.89
can = canvas.Canvas(packet, pagesize=A4)

def convert_y(y_from_top):
    return page_height - y_from_top

# Test different font sizes and positions
can.setFont("Helvetica", 9)

# The 9 SDL boxes (boxes 2-10)
boxes_x = [440.4, 454.6, 468.8, 482.9, 497.1, 511.3, 525.5, 539.6, 553.8]
y_pos = convert_y(333.3)

# Draw the digits
sdl_digits = "820714253"
for i, digit in enumerate(sdl_digits):
    # Need to adjust x to center the character in the box
    # Get text width and offset to center
    text_width = can.stringWidth(digit, "Helvetica", 9)
    x_centered = boxes_x[i] - (text_width / 2)
    can.drawString(x_centered, y_pos, digit)

# Also test marking the exact center points with dots for verification
can.setFillColorRGB(1, 0, 0)  # Red dots
for x in boxes_x:
    can.circle(x, y_pos + 2, 1, fill=1)

can.save()
packet.seek(0)

# Merge with original
overlay_pdf = PdfReader(packet)
original_pdf = PdfReader('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
writer = PdfWriter()

page = original_pdf.pages[0]
page.merge_page(overlay_pdf.pages[0])
writer.add_page(page)

for i in range(1, len(original_pdf.pages)):
    writer.add_page(original_pdf.pages[i])

with open('test_sdl_centering.pdf', 'wb') as output_file:
    writer.write(output_file)

print("Test PDF created: test_sdl_centering.pdf")
print("Red dots mark the box centers - digits should be centered on these dots")
