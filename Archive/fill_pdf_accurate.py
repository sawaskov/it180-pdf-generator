import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

def create_overlay(data):
    """Create an overlay PDF with correct field positions"""
    packet = io.BytesIO()

    # A4 size
    page_height = 841.89
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)

    # Convert from PDF coordinates (top-origin) to ReportLab coordinates (bottom-origin)
    def convert_y(y_from_top):
        return page_height - y_from_top

    # Tax Reference Number boxes (top right)
    # 10 boxes for tax reference number, one digit per box
    # Boxes are at x: 344.6, 358.8, 373.0, 387.1, 401.3, 415.5, 429.6, 443.8, 458.0, 472.2
    # Y position: 172.3 to 186.5 (center at ~179)
    tax_ref = str(data['tax_ref']).zfill(10)
    x_start = 348  # Center of first box
    y_pos = convert_y(182)  # Center vertically in the boxes
    box_width = 14.17  # Width of each box

    for i, digit in enumerate(tax_ref[:10]):
        can.drawString(x_start + (i * box_width), y_pos, digit)

    # Year of Assessment boxes
    # Field is around y=200 from top, boxes start around x=507
    year = str(data['year'])
    x_start = 507
    y_pos = convert_y(217)
    for i, digit in enumerate(year):
        can.drawString(x_start + (i * 11.5), y_pos, digit)

    # Registered name of employer
    # Label at y=272-280, input field below
    can.drawString(40, convert_y(295), str(data['employer_name']))

    # SDL reference number (with L prefix)
    # Label at y=327-335, boxes on right side around x=653
    sdl_ref = str(data['sdl_ref']).replace('L', '').zfill(10)
    x_start = 653
    y_pos = convert_y(343)
    for i, digit in enumerate(sdl_ref[:10]):
        can.drawString(x_start + (i * 11.5), y_pos, digit)

    # Name of SETA
    # Label at y=349-357, input below
    can.drawString(40, convert_y(373), str(data['seta_name']))

    # Particulars of title and code
    # Label at y=403-411, input below
    if data['learnership_title'] and str(data['learnership_title']) != 'nan':
        can.drawString(40, convert_y(427), str(data['learnership_title']))

    # Full names and identity number of learner
    # Label at y=470-478, input below
    can.drawString(40, convert_y(494), str(data['learner_full']))

    # ID number boxes (below the name field)
    # Boxes appear to be around y=505
    if data['learner_id']:
        id_num = str(data['learner_id']).replace('-', '')[:13]
        x_start = 40
        y_pos = convert_y(513)
        for i, digit in enumerate(id_num[:13]):
            can.drawString(x_start + (i * 14.5), y_pos, digit)

    # Date of entering (start date)
    # Label at y=525-533, date boxes on right around x=690
    if isinstance(data['start_date'], pd.Timestamp):
        date_str = data['start_date'].strftime('%Y%m%d')
        y_pos = convert_y(543)
        # CCYY
        x_start = 690
        for i in range(4):
            can.drawString(x_start + (i * 11.5), y_pos, date_str[i])
        # MM
        x_start = 750
        for i in range(2):
            can.drawString(x_start + (i * 11.5), y_pos, date_str[4+i])
        # DD
        x_start = 785
        for i in range(2):
            can.drawString(x_start + (i * 11.5), y_pos, date_str[6+i])

    # Date of completion (end date)
    # Label at y=548-556, date boxes on right
    if isinstance(data['end_date'], pd.Timestamp):
        date_str = data['end_date'].strftime('%Y%m%d')
        y_pos = convert_y(567)
        # CCYY
        x_start = 690
        for i in range(4):
            can.drawString(x_start + (i * 11.5), y_pos, date_str[i])
        # MM
        x_start = 750
        for i in range(2):
            can.drawString(x_start + (i * 11.5), y_pos, date_str[4+i])
        # DD
        x_start = 785
        for i in range(2):
            can.drawString(x_start + (i * 11.5), y_pos, date_str[6+i])

    # Was employed checkbox (around y=581-589)
    can.setFont("Helvetica", 10)
    y_pos = convert_y(597)
    if data['was_employed'] == 'Y':
        can.drawString(820, y_pos, 'X')  # YES
    else:
        can.drawString(850, y_pos, 'X')  # NO

    # Was disabled checkbox (around y=622-630)
    y_pos = convert_y(638)
    if data['was_disabled'] == 'Y':
        can.drawString(820, y_pos, 'X')  # YES
    else:
        can.drawString(850, y_pos, 'X')  # NO

    # In course of trade checkbox (around y=648-656)
    y_pos = convert_y(664)
    if data['in_trade'] == 'Y':
        can.drawString(820, y_pos, 'X')  # YES
    else:
        can.drawString(850, y_pos, 'X')  # NO

    # Period (months) - around y=673-681
    can.setFont("Helvetica", 9)
    months = str(data['period_months'])
    x_start = 302
    y_pos = convert_y(687)
    for i, digit in enumerate(months[:3]):
        can.drawString(x_start + (i * 11.5), y_pos, digit)

    # Annual remuneration - around y=699-707
    # R boxes start around x=525
    remuneration = str(int(data['annual_remuneration'])).zfill(12)
    x_start = 525
    y_pos = convert_y(734)
    for i, digit in enumerate(remuneration[:12]):
        can.drawString(x_start + (i * 11.5), y_pos, digit)

    # Deduction claimed - around y=754-762
    deduction = str(int(data['deduction_claimed'])).zfill(12)
    x_start = 525
    y_pos = convert_y(769)
    for i, digit in enumerate(deduction[:12]):
        can.drawString(x_start + (i * 11.5), y_pos, digit)

    # Limitation - around y=778-786
    limitation = str(int(data['limitation'])).zfill(12)
    x_start = 525
    y_pos = convert_y(793)
    for i, digit in enumerate(limitation[:12]):
        can.drawString(x_start + (i * 11.5), y_pos, digit)

    can.save()
    packet.seek(0)
    return packet

def populate_pdf_for_row(row_data, row_number):
    """Populate PDF with data from a single row"""

    learner_full = str(row_data['Full names and identity number of the learner contemplated in the registered learnership agreement']) if pd.notna(row_data['Full names and identity number of the learner contemplated in the registered learnership agreement']) else ''

    # Split name and ID
    parts = learner_full.rsplit(' ', 1) if learner_full else ['', '']
    learner_name = parts[0] if len(parts) > 1 else learner_full
    learner_id = parts[1] if len(parts) > 1 else ''

    data = {
        'tax_ref': str(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) if pd.notna(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) else '',
        'year': str(int(row_data['Year of Assessment'])) if pd.notna(row_data['Year of Assessment']) else '',
        'employer_name': str(row_data['Geregistreerde naam van werkgewer']) if pd.notna(row_data['Geregistreerde naam van werkgewer']) else '',
        'sdl_ref': str(row_data['Skills Development Levy reference number']) if pd.notna(row_data['Skills Development Levy reference number']) else '',
        'seta_name': str(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) if pd.notna(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) else '',
        'learnership_title': str(row_data['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) if pd.notna(row_data['Particulars of title and code allocated and issued by the DirectorGeneral Department of Labour in terms of regulation 23 of the Learnership']) else '',
        'learner_full': learner_full,
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

    overlay_packet = create_overlay(data)
    overlay_pdf = PdfReader(overlay_packet)
    original_pdf = PdfReader('IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
    writer = PdfWriter()

    page = original_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    for i in range(1, len(original_pdf.pages)):
        writer.add_page(original_pdf.pages[i])

    safe_name = learner_name.replace(" ", "_")[:20] if learner_name else "Unknown"
    output_filename = f'IT180_Accurate_Row{row_number}_{safe_name}.pdf'

    with open(output_filename, 'wb') as output_file:
        writer.write(output_file)

    return output_filename

if __name__ == '__main__':
    df = pd.read_excel('PEG 12H allowance - FY2025 (2).xlsx')
    print(f"Found {len(df)} rows in Excel file")
    print("\nProcessing Row 1 with accurately positioned fields...")

    row = df.iloc[0]
    output_file = populate_pdf_for_row(row, 1)

    print(f"\nPDF created: {output_file}")
    print("Fields positioned based on exact PDF coordinate analysis.")
