import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime

def create_overlay(data):
    """Create an overlay PDF with the form data positioned correctly"""
    packet = io.BytesIO()

    # A4 size is 595.27 x 841.89 points
    can = canvas.Canvas(packet, pagesize=A4)

    # Set font size to 9 for form fields
    can.setFont("Helvetica", 9)

    # Page 1 - Main form fields
    # Lowered all Y coordinates by 50 points to position fields correctly

    # Income Tax Reference Number (top right, individual boxes)
    tax_ref = str(data['tax_ref'])
    x_start = 540
    y_pos = 730
    for i, digit in enumerate(tax_ref):
        can.drawString(x_start + (i * 10.5), y_pos, digit)

    # Year of Assessment (boxes below tax ref)
    year = str(data['year'])
    y_pos = 710
    x_start = 540
    for i, digit in enumerate(year):
        can.drawString(x_start + (i * 10.5), y_pos, digit)

    # Registered name of employer (long field)
    can.drawString(60, 660, str(data['employer_name']))

    # SDL reference number (with L prefix and boxes)
    sdl_ref = str(data['sdl_ref']).replace('L', '')
    can.drawString(667, 635, 'L')
    x_start = 680
    for i, digit in enumerate(sdl_ref):
        if i < 10:  # Limit to available boxes
            can.drawString(x_start + (i * 10.5), 635, digit)

    # Name of SETA
    can.drawString(60, 610, str(data['seta_name']))

    # Particulars of title and code (learnership title)
    if data['learnership_title']:
        can.drawString(60, 580, str(data['learnership_title']))

    # Full names and identity number of learner
    learner_info = str(data['learner_name_id'])
    can.drawString(60, 545, learner_info)

    # Identity number boxes (if we have it separately)
    # For now, included in the line above

    # Start date (CCYY-MM-DD format in boxes)
    if isinstance(data['start_date'], pd.Timestamp):
        start_date_str = data['start_date'].strftime('%Y%m%d')
        # CCYY
        x_start = 690
        for i in range(4):
            can.drawString(x_start + (i * 10.5), 490, start_date_str[i])
        # MM
        x_start = 750
        for i in range(2):
            can.drawString(x_start + (i * 10.5), 490, start_date_str[4+i])
        # DD
        x_start = 785
        for i in range(2):
            can.drawString(x_start + (i * 10.5), 490, start_date_str[6+i])

    # End date (CCYY-MM-DD format in boxes)
    if isinstance(data['end_date'], pd.Timestamp):
        end_date_str = data['end_date'].strftime('%Y%m%d')
        # CCYY
        x_start = 690
        for i in range(4):
            can.drawString(x_start + (i * 10.5), 460, end_date_str[i])
        # MM
        x_start = 750
        for i in range(2):
            can.drawString(x_start + (i * 10.5), 460, end_date_str[4+i])
        # DD
        x_start = 785
        for i in range(2):
            can.drawString(x_start + (i * 10.5), 460, end_date_str[6+i])

    # Was employed? YES/NO checkboxes
    if data['was_employed'] == 'Y':
        can.drawString(820, 425, 'X')  # YES checkbox
    else:
        can.drawString(820, 410, 'X')  # NO checkbox

    # Was disabled? YES/NO checkboxes
    if data['was_disabled'] == 'Y':
        can.drawString(820, 395, 'X')  # YES checkbox
    else:
        can.drawString(820, 380, 'X')  # NO checkbox

    # In course of trade? YES/NO checkboxes
    if data['in_trade'] == 'Y':
        can.drawString(820, 365, 'X')  # YES checkbox
    else:
        can.drawString(820, 350, 'X')  # NO checkbox

    # Period of learnership (months) - boxes
    months = str(int(data['annual_remuneration'])) if data['annual_remuneration'] else '12'
    x_start = 330
    for i, digit in enumerate(months):
        if i < 3:
            can.drawString(x_start + (i * 10.5), 335, digit)

    # Annual remuneration (R boxes)
    remuneration = str(int(data['annual_remuneration'])) if data['annual_remuneration'] else '0'
    x_start = 540
    # Right align the number in the boxes
    for i, digit in enumerate(remuneration[-12:] if len(remuneration) > 12 else remuneration):
        can.drawString(x_start + (i * 10.5), 300, digit)

    # Deduction claimed (R boxes)
    deduction = str(int(data['deduction_claimed'])) if data['deduction_claimed'] else '0'
    x_start = 540
    for i, digit in enumerate(deduction[-12:] if len(deduction) > 12 else deduction):
        can.drawString(x_start + (i * 10.5), 270, digit)

    # Limitation (R boxes)
    limitation = str(int(data['limitation'])) if data['limitation'] else '0'
    x_start = 540
    for i, digit in enumerate(limitation[-12:] if len(limitation) > 12 else limitation):
        can.drawString(x_start + (i * 10.5), 240, digit)

    can.save()
    packet.seek(0)
    return packet

def populate_pdf_for_row(row_data, row_number):
    """Populate PDF with data from a single row"""

    # Prepare data dictionary
    data = {
        'tax_ref': str(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) if pd.notna(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) else '',
        'year': str(int(row_data['Year of Assessment'])) if pd.notna(row_data['Year of Assessment']) else '',
        'employer_name': str(row_data['Geregistreerde naam van werkgewer']) if pd.notna(row_data['Geregistreerde naam van werkgewer']) else '',
        'sdl_ref': str(row_data['Skills Development Levy reference number']) if pd.notna(row_data['Skills Development Levy reference number']) else '',
        'seta_name': str(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) if pd.notna(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) else '',
        'learnership_title': str(row_data['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) if pd.notna(row_data['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) else '',
        'learner_name_id': str(row_data['Full names and identity number of the learner contemplated in the registered learnership agreement']) if pd.notna(row_data['Full names and identity number of the learner contemplated in the registered learnership agreement']) else '',
        'start_date': row_data['Start date'],
        'end_date': row_data['End date'],
        'was_employed': str(row_data['Was the learner at the time of entering into the learnership agreement employed']) if pd.notna(row_data['Was the learner at the time of entering into the learnership agreement employed']) else 'N',
        'was_disabled': str(row_data['Was the learner at the time of entering into the learnership agreement, a disabled person?']) if pd.notna(row_data['Was the learner at the time of entering into the learnership agreement, a disabled person?']) else 'N',
        'in_trade': str(row_data['Was the learnership agreement entered into between the employer and the learner in the course of any trade carried on by that employer?']) if pd.notna(row_data['Was the learnership agreement entered into between the employer and the learner in the course of any trade carried on by that employer?']) else 'N',
        'annual_remuneration': float(row_data['The annual equivalent or the total remuneration as stipulated in the employment']) if pd.notna(row_data['The annual equivalent or the total remuneration as stipulated in the employment']) else 0.0,
        'deduction_claimed': float(row_data['Rands only_2']) if pd.notna(row_data['Rands only_2']) else 0.0,
        'limitation': float(row_data['Rands only_3']) if pd.notna(row_data['Rands only_3']) else 0.0,
    }

    # Create overlay
    overlay_packet = create_overlay(data)
    overlay_pdf = PdfReader(overlay_packet)

    # Read original PDF
    original_pdf = PdfReader('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')

    # Create writer
    writer = PdfWriter()

    # Merge overlay with original first page
    page = original_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    # Add remaining pages
    for i in range(1, len(original_pdf.pages)):
        writer.add_page(original_pdf.pages[i])

    # Generate output filename
    learner_id = data['learner_name_id'].replace(" ", "_")[:30]
    output_filename = f'IT180_Corrected_Row{row_number}_{learner_id}.pdf'

    # Save
    with open(output_filename, 'wb') as output_file:
        writer.write(output_file)

    return output_filename

# Main execution
if __name__ == '__main__':
    # Read Excel file
    df = pd.read_excel('PEG 12H allowance - FY2025 (2).xlsx')

    print(f"Found {len(df)} rows in Excel file")
    print("\nProcessing Row 1...")

    # Process first row
    row = df.iloc[0]
    output_file = populate_pdf_for_row(row, 1)

    print(f"\nPDF created successfully: {output_file}")
    print("\nPlease review the corrected PDF.")
    print("If fields are still misaligned, I can adjust the coordinates further.")
