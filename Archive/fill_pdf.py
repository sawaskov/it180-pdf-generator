import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from datetime import datetime

def create_overlay(data):
    """Create an overlay PDF with the form data"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Set font
    can.setFont("Helvetica", 10)

    # Tax reference number (top section)
    can.drawString(180, 770, str(data['tax_ref']))

    # Year of assessment
    can.drawString(480, 770, str(data['year']))

    # Employer name
    can.drawString(150, 730, str(data['employer_name']))

    # SDL reference number
    can.drawString(400, 730, str(data['sdl_ref']))

    # SETA name
    can.drawString(150, 690, str(data['seta_name']))

    # Learnership title and code
    if pd.notna(data['learnership_title']):
        can.drawString(150, 650, str(data['learnership_title']))

    # Learner name and ID
    can.drawString(150, 610, str(data['learner_name_id']))

    # Start date
    start_date = data['start_date']
    if isinstance(start_date, pd.Timestamp):
        can.drawString(150, 570, start_date.strftime('%Y-%m-%d'))

    # End date
    end_date = data['end_date']
    if isinstance(end_date, pd.Timestamp):
        can.drawString(300, 570, end_date.strftime('%Y-%m-%d'))

    # Checkboxes - Was employed (Y/N)
    if data['was_employed'] == 'Y':
        can.drawString(150, 530, 'X')  # Yes checkbox
    else:
        can.drawString(200, 530, 'X')  # No checkbox

    # Was disabled (Y/N)
    if data['was_disabled'] == 'Y':
        can.drawString(150, 500, 'X')  # Yes checkbox
    else:
        can.drawString(200, 500, 'X')  # No checkbox

    # In course of trade (Y/N)
    if data['in_trade'] == 'Y':
        can.drawString(150, 470, 'X')  # Yes checkbox
    else:
        can.drawString(200, 470, 'X')  # No checkbox

    # Annual remuneration
    can.drawString(400, 440, f"R {data['annual_remuneration']:,.2f}")

    # Deduction claimed
    can.drawString(400, 410, f"R {data['deduction_claimed']:,.2f}")

    # Limitation
    can.drawString(400, 380, f"R {data['limitation']:,.2f}")

    # Signature section (leave blank for manual signing)
    # can.drawString(150, 150, str(data['signature']))

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

    # Merge overlay with original
    page = original_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    # Add remaining pages if any
    for i in range(1, len(original_pdf.pages)):
        writer.add_page(original_pdf.pages[i])

    # Generate output filename
    learner_id = data['learner_name_id'].replace(" ", "_")[:30]
    output_filename = f'IT180_Row{row_number}_{learner_id}.pdf'

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
    print("\nPlease review the PDF to check if the data is positioned correctly.")
    print("If adjustments are needed, let me know which fields need repositioning.")
