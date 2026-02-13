import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def create_overlay(data):
    """Create an overlay PDF with the form data positioned correctly"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 8)

    # Income Tax Reference Number (top right, in boxes)
    # Position needs to be in the small boxes at top right
    tax_ref = str(data['tax_ref']).zfill(10)  # Pad to 10 digits
    x_start = 539
    y_pos = 733
    for i, digit in enumerate(tax_ref):
        can.drawString(x_start + (i * 10.8), y_pos, digit)

    # Year of Assessment (4 boxes below tax ref)
    year = str(data['year'])
    x_start = 539
    y_pos = 713
    for i, digit in enumerate(year):
        can.drawString(x_start + (i * 10.8), y_pos, digit)

    # Registered name of employer (in the blue field area)
    can.setFont("Helvetica", 9)
    can.drawString(55, 447, str(data['employer_name']))

    # SDL reference number (with L prefix in boxes on right)
    sdl_ref = str(data['sdl_ref']).replace('L', '').zfill(10)
    can.setFont("Helvetica", 8)
    x_start = 676
    y_pos = 509
    for i, digit in enumerate(sdl_ref):
        can.drawString(x_start + (i * 10.8), y_pos, digit)

    # Name of SETA (in blue field)
    can.setFont("Helvetica", 9)
    can.drawString(55, 546, str(data['seta_name']))

    # Particulars of title and code (in blue field)
    if data['learnership_title'] and str(data['learnership_title']) != 'nan':
        can.drawString(55, 640, str(data['learnership_title']))

    # Full names and identity number of learner (in blue field)
    can.drawString(55, 734, str(data['learner_name']))

    # ID number in boxes
    id_number = str(data['learner_id']).replace('-', '')[:13]
    x_start = 55
    y_pos = 783
    for i, digit in enumerate(id_number):
        if i < 13:
            can.drawString(x_start + (i * 13), y_pos, digit)

    # Date of entering into agreement (Start date - CCYY-MM-DD in boxes on right)
    if isinstance(data['start_date'], pd.Timestamp):
        start_date_str = data['start_date'].strftime('%Y%m%d')
        can.setFont("Helvetica", 8)
        # CCYY
        x_start = 693
        y_pos = 820
        for i in range(4):
            can.drawString(x_start + (i * 10.8), y_pos, start_date_str[i])
        # MM
        x_start = 756
        for i in range(2):
            can.drawString(x_start + (i * 10.8), y_pos, start_date_str[4+i])
        # DD
        x_start = 789
        for i in range(2):
            can.drawString(x_start + (i * 10.8), y_pos, start_date_str[6+i])

    # Date of completion (End date - CCYY-MM-DD in boxes on right)
    if isinstance(data['end_date'], pd.Timestamp):
        end_date_str = data['end_date'].strftime('%Y%m%d')
        can.setFont("Helvetica", 8)
        # CCYY
        x_start = 693
        y_pos = 869
        for i in range(4):
            can.drawString(x_start + (i * 10.8), y_pos, end_date_str[i])
        # MM
        x_start = 756
        for i in range(2):
            can.drawString(x_start + (i * 10.8), y_pos, end_date_str[4+i])
        # DD
        x_start = 789
        for i in range(2):
            can.drawString(x_start + (i * 10.8), y_pos, end_date_str[6+i])

    # Was employed? YES/NO
    can.setFont("Helvetica", 10)
    if data['was_employed'] == 'Y':
        can.drawString(827, 908, 'X')
    else:
        can.drawString(856, 908, 'X')

    # Was disabled? YES/NO
    if data['was_disabled'] == 'Y':
        can.drawString(827, 943, 'X')
    else:
        can.drawString(856, 943, 'X')

    # In course of trade? YES/NO
    if data['in_trade'] == 'Y':
        can.drawString(827, 1010, 'X')
    else:
        can.drawString(856, 1010, 'X')

    # Period of learnership (months) - in boxes on left
    period_months = str(data['period_months'])
    can.setFont("Helvetica", 8)
    x_start = 306
    y_pos = 1040
    for i, digit in enumerate(period_months):
        if i < 3:
            can.drawString(x_start + (i * 10.8), y_pos, digit)

    # Annual remuneration (R amount in boxes)
    remuneration_str = str(int(data['annual_remuneration'])).zfill(12)
    x_start = 535
    y_pos = 1100
    for i, digit in enumerate(remuneration_str):
        if i < 12:
            can.drawString(x_start + (i * 10.8), y_pos, digit)

    # Deduction claimed (R amount in boxes)
    deduction_str = str(int(data['deduction_claimed'])).zfill(12)
    x_start = 535
    y_pos = 1154
    for i, digit in enumerate(deduction_str):
        if i < 12:
            can.drawString(x_start + (i * 10.8), y_pos, digit)

    # Limitation (R amount in boxes)
    limitation_str = str(int(data['limitation'])).zfill(12)
    x_start = 535
    y_pos = 1208
    for i, digit in enumerate(limitation_str):
        if i < 12:
            can.drawString(x_start + (i * 10.8), y_pos, digit)

    can.save()
    packet.seek(0)
    return packet

def populate_pdf_for_row(row_data, row_number):
    """Populate PDF with data from a single row"""

    # Extract learner name and ID separately
    learner_full = str(row_data['Full names and identity number of the learner contemplated in the registered learnership agreement']) if pd.notna(row_data['Full names and identity number of the learner contemplated in the registered learnership agreement']) else ''

    # Try to split name and ID - assuming format "Name Surname ID"
    parts = learner_full.rsplit(' ', 1) if learner_full else ['', '']
    learner_name = parts[0] if len(parts) > 1 else learner_full
    learner_id = parts[1] if len(parts) > 1 else ''

    # Prepare data dictionary
    data = {
        'tax_ref': str(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) if pd.notna(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) else '',
        'year': str(int(row_data['Year of Assessment'])) if pd.notna(row_data['Year of Assessment']) else '',
        'employer_name': str(row_data['Geregistreerde naam van werkgewer']) if pd.notna(row_data['Geregistreerde naam van werkgewer']) else '',
        'sdl_ref': str(row_data['Skills Development Levy reference number']) if pd.notna(row_data['Skills Development Levy reference number']) else '',
        'seta_name': str(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) if pd.notna(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) else '',
        'learnership_title': str(row_data['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) if pd.notna(row_data['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) else '',
        'learner_name': learner_name,
        'learner_id': learner_id,
        'start_date': row_data['Start date'],
        'end_date': row_data['End date'],
        'was_employed': str(row_data['Was the learner at the time of entering into the learnership agreement employed']) if pd.notna(row_data['Was the learner at the time of entering into the learnership agreement employed']) else 'N',
        'was_disabled': str(row_data['Was the learner at the time of entering into the learnership agreement, a disabled person?']) if pd.notna(row_data['Was the learner at the time of entering into the learnership agreement, a disabled person?']) else 'N',
        'in_trade': str(row_data['Was the learnership agreement entered into between the employer and the learner in the course of any trade carried on by that employer?']) if pd.notna(row_data['Was the learnership agreement entered into between the employer and the learner in the course of any trade carried on by that employer?']) else 'N',
        'period_months': int(row_data['The annual equivalent or the total remuneration as stipulated in the employment']) if pd.notna(row_data['The annual equivalent or the total remuneration as stipulated in the employment']) else 12,
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
    safe_name = learner_name.replace(" ", "_")[:20] if learner_name else "Unknown"
    output_filename = f'IT180_Final_Row{row_number}_{safe_name}.pdf'

    # Save
    with open(output_filename, 'wb') as output_file:
        writer.write(output_file)

    return output_filename

# Main execution
if __name__ == '__main__':
    # Read Excel file
    df = pd.read_excel('PEG 12H allowance - FY2025 (2).xlsx')

    print(f"Found {len(df)} rows in Excel file")
    print("\nProcessing Row 1 with corrected field positions...")

    # Process first row
    row = df.iloc[0]
    output_file = populate_pdf_for_row(row, 1)

    print(f"\nPDF created: {output_file}")
    print("\nThis version has completely remapped all fields.")
    print("Please review and let me know if it's correct now.")
