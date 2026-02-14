from flask import Flask, render_template, request, send_file, jsonify, session, after_this_request
import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime
import re
import os
import zipfile
import tempfile
import shutil
import threading
import time
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='Templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['OUTPUT_FOLDER'] = tempfile.mkdtemp()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(text):
    """Remove special characters, replace tabs with spaces, clean text for PDF"""
    if not text or pd.isna(text):
        return ''
    text = str(text)
    # Replace tabs with spaces
    text = text.replace('\t', ' ')
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove other control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in ['\n', '\r'])
    # Strip leading/trailing whitespace
    return text.strip()

def create_overlay(data):
    """Create an overlay PDF with all fields correctly positioned in their boxes"""
    packet = io.BytesIO()
    page_height = 841.89
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)

    def convert_y(y_from_top):
        return page_height - y_from_top

    # ===== TAX REFERENCE NUMBER (10 boxes) =====
    tax_ref = str(data['tax_ref']).zfill(10)
    x_start = 348
    y_pos = convert_y(182)
    box_width = 14.17
    for i, digit in enumerate(tax_ref[:10]):
        can.drawString(x_start + (i * box_width), y_pos, digit)

    # ===== YEAR OF ASSESSMENT (4 boxes) =====
    year = str(data['year'])
    boxes_x = [433, 447, 461, 475]  # Centers of the 4 boxes
    y_pos = convert_y(202)
    for i, digit in enumerate(year[:4]):
        can.drawString(boxes_x[i], y_pos, digit)

    # ===== REGISTERED NAME OF EMPLOYER (text field) =====
    # White block center at y=296.7
    can.drawString(40, convert_y(296.7) - 3, clean_text(data['employer_name']))

    # ===== SDL REFERENCE NUMBER (boxes after L) =====
    # 10 boxes total, first has L, use boxes 2-10 for the 9 digits
    sdl_ref = str(data['sdl_ref']).replace('L', '').strip()
    boxes_x = [440.4, 454.6, 468.8, 482.9, 497.1, 511.3, 525.5, 539.6, 553.8]  # Boxes 2-10
    # Boxes are at y=326.2 to 340.4, center at 333.3
    # Adjust for text baseline - text should be positioned lower to appear centered
    y_pos = convert_y(333.3) - 3  # Offset for vertical centering
    for i, digit in enumerate(sdl_ref[:9]):
        # Center the digit in the box horizontally
        text_width = can.stringWidth(digit, "Helvetica", 9)
        x_centered = boxes_x[i] - (text_width / 2)
        can.drawString(x_centered, y_pos, digit)

    # ===== NAME OF SETA (text field) =====
    # White block center at y=373.0
    can.drawString(40, convert_y(373.0) - 3, clean_text(data['seta_name']))

    # ===== LEARNERSHIP TITLE (text field) =====
    # White block center at y=443.0
    if data['learnership_title'] and str(data['learnership_title']) != 'nan':
        can.drawString(40, convert_y(443.0) - 3, clean_text(data['learnership_title']))

    # ===== LEARNERSHIP CODE (text field) =====
    # White block center at y=458.9
    if data['learnership_code'] and str(data['learnership_code']) != 'nan':
        can.drawString(40, convert_y(458.9) - 3, clean_text(data['learnership_code']))

    # ===== LEARNER FULL NAME (text field) =====
    # White block center at y=494.7
    can.drawString(40, convert_y(494.7) - 3, clean_text(data['learner_name']))

    # ===== ID NUMBER (13 boxes) =====
    if data['learner_id']:
        id_num = str(data['learner_id']).replace('-', '').replace(' ', '')[:13]
        x_start = 38
        y_pos = convert_y(513)
        box_width = 14.17
        for i, digit in enumerate(id_num[:13]):
            can.drawString(x_start + (i * box_width), y_pos, digit)

    # ===== START DATE (CCYY-MM-DD in boxes) =====
    if isinstance(data['start_date'], pd.Timestamp):
        date_str = data['start_date'].strftime('%Y%m%d')
        y_pos = convert_y(532.1) - 3  # Center Y with baseline offset

        # CCYY: 4 digits
        ccyy_x = [446.2, 458.2, 470.1, 482.1]
        for i in range(4):
            text_width = can.stringWidth(date_str[i], "Helvetica", 9)
            x_centered = ccyy_x[i] - (text_width / 2)
            can.drawString(x_centered, y_pos, date_str[i])

        # MM: 2 digits
        mm_x = [506.6, 518.6]
        for i in range(2):
            text_width = can.stringWidth(date_str[4+i], "Helvetica", 9)
            x_centered = mm_x[i] - (text_width / 2)
            can.drawString(x_centered, y_pos, date_str[4+i])

        # DD: 2 digits
        dd_x = [542.8, 554.8]
        for i in range(2):
            text_width = can.stringWidth(date_str[6+i], "Helvetica", 9)
            x_centered = dd_x[i] - (text_width / 2)
            can.drawString(x_centered, y_pos, date_str[6+i])

    # ===== END DATE (CCYY-MM-DD in boxes) =====
    if isinstance(data['end_date'], pd.Timestamp):
        date_str = data['end_date'].strftime('%Y%m%d')
        y_pos = convert_y(562.7) - 3  # Center Y with baseline offset

        # CCYY: 4 digits
        ccyy_x = [446.2, 458.2, 470.1, 482.1]
        for i in range(4):
            text_width = can.stringWidth(date_str[i], "Helvetica", 9)
            x_centered = ccyy_x[i] - (text_width / 2)
            can.drawString(x_centered, y_pos, date_str[i])

        # MM: 2 digits
        mm_x = [506.6, 518.6]
        for i in range(2):
            text_width = can.stringWidth(date_str[4+i], "Helvetica", 9)
            x_centered = mm_x[i] - (text_width / 2)
            can.drawString(x_centered, y_pos, date_str[4+i])

        # DD: 2 digits
        dd_x = [542.8, 554.8]
        for i in range(2):
            text_width = can.stringWidth(date_str[6+i], "Helvetica", 9)
            x_centered = dd_x[i] - (text_width / 2)
            can.drawString(x_centered, y_pos, date_str[6+i])

    # ===== CHECKBOXES ON PAGE 1 =====
    can.setFont("Helvetica", 10)

    # Calculate centered X positions for checkboxes
    # YES box: X=497.6 to 529.5 (center: 513.6)
    # NO box: X=529.5 to 561.4 (center: 545.5)
    x_width = can.stringWidth('X', "Helvetica", 10)
    yes_x = 513.6 - (x_width / 2)
    no_x = 545.5 - (x_width / 2)

    # 1. Was employed? (Y=602.5)
    y_pos = convert_y(602.5) - 3
    if data['was_employed'] == 'Y':
        can.drawString(yes_x, y_pos, 'X')
    else:
        can.drawString(no_x, y_pos, 'X')

    # 2. Was disabled? (Y=628.3)
    y_pos = convert_y(628.3) - 3
    if data['was_disabled'] == 'Y':
        can.drawString(yes_x, y_pos, 'X')
    else:
        can.drawString(no_x, y_pos, 'X')

    # 3. In course of trade? (Y=654.2)
    y_pos = convert_y(654.2) - 3
    if data['in_trade'] == 'Y':
        can.drawString(yes_x, y_pos, 'X')
    else:
        can.drawString(no_x, y_pos, 'X')

    # ===== PERIOD (MONTHS) - 2 boxes =====
    can.setFont("Helvetica", 9)
    months = str(data['period_months']).zfill(2)
    boxes_x = [183, 197]
    y_pos = convert_y(684)
    for i, digit in enumerate(months[:2]):
        can.drawString(boxes_x[i], y_pos, digit)

    # ===== ANNUAL REMUNERATION (R boxes - 7 visible boxes) =====
    # No leading zeros - right-align the number
    # Only populate if value is not 0 (blank/NULL)
    if data['annual_remuneration'] > 0:
        remuneration = str(int(data['annual_remuneration']))
        boxes_x = [414, 430, 442, 455, 470, 483, 496]
        y_pos = convert_y(740)
        # Start from the rightmost box and work backwards
        for i in range(len(remuneration)):
            digit_pos = len(remuneration) - 1 - i  # Position in the number string (from right)
            box_pos = 6 - i  # Position in boxes array (from right)
            if box_pos >= 0:
                can.drawString(boxes_x[box_pos], y_pos, remuneration[digit_pos])

    # ===== DEDUCTION CLAIMED (R boxes - 7 visible boxes) =====
    # Only populate if value is not 0 (blank/NULL)
    if data['deduction_claimed'] > 0:
        deduction = str(int(data['deduction_claimed']))
        boxes_x = [414, 430, 442, 455, 470, 483, 496]
        y_pos = convert_y(764)
        for i in range(len(deduction)):
            digit_pos = len(deduction) - 1 - i
            box_pos = 6 - i
            if box_pos >= 0:
                can.drawString(boxes_x[box_pos], y_pos, deduction[digit_pos])

    # ===== LIMITATION (R boxes - 7 visible boxes) =====
    # Only populate if value is not 0 (blank/NULL)
    if data['limitation'] > 0:
        limitation = str(int(data['limitation']))
        boxes_x = [414, 430, 442, 455, 470, 483, 496]
        y_pos = convert_y(788)
        for i in range(len(limitation)):
            digit_pos = len(limitation) - 1 - i
            box_pos = 6 - i
            if box_pos >= 0:
                can.drawString(boxes_x[box_pos], y_pos, limitation[digit_pos])

    can.save()
    packet.seek(0)
    return packet

def create_page2_overlay(data):
    """Create overlay for page 2 with today's date and checkboxes"""
    packet = io.BytesIO()
    page_height = 841.89
    can = canvas.Canvas(packet, pagesize=A4)

    def convert_y(y_from_top):
        return page_height - y_from_top

    can.setFont("Helvetica", 9)

    # ===== REPRESENTATIVE NAME (text field on page 2) =====
    # White block center at y=204.1
    if data.get('representative_name'):
        can.drawString(45, convert_y(204.1) - 3, clean_text(data['representative_name']))

    # Get today's date
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')

    # Date boxes on page 2 at Y=261.7
    # CCYY box: 440.2-488.1, MM box: 500.6-524.6, DD box: 536.8-560.8
    y_pos = convert_y(261.7) - 3  # Center Y with baseline offset

    # CCYY: 4 digits (calculated center positions)
    ccyy_start = 440.2
    ccyy_width = 47.9
    digit_width = ccyy_width / 4
    ccyy_x = [ccyy_start + (i * digit_width) + (digit_width / 2) for i in range(4)]

    for i in range(4):
        text_width = can.stringWidth(date_str[i], "Helvetica", 9)
        x_centered = ccyy_x[i] - (text_width / 2)
        can.drawString(x_centered, y_pos, date_str[i])

    # MM: 2 digits
    mm_start = 500.6
    mm_width = 24.0
    mm_digit_width = mm_width / 2
    mm_x = [mm_start + (i * mm_digit_width) + (mm_digit_width / 2) for i in range(2)]

    for i in range(2):
        text_width = can.stringWidth(date_str[4+i], "Helvetica", 9)
        x_centered = mm_x[i] - (text_width / 2)
        can.drawString(x_centered, y_pos, date_str[4+i])

    # DD: 2 digits
    dd_start = 536.8
    dd_width = 24.0
    dd_digit_width = dd_width / 2
    dd_x = [dd_start + (i * dd_digit_width) + (dd_digit_width / 2) for i in range(2)]

    for i in range(2):
        text_width = can.stringWidth(date_str[6+i], "Helvetica", 9)
        x_centered = dd_x[i] - (text_width / 2)
        can.drawString(x_centered, y_pos, date_str[6+i])

    # ===== CHECKBOXES ON PAGE 2 =====
    can.setFont("Helvetica", 10)

    # Calculate centered X positions for checkboxes
    # YES box: X=497.6 to 529.5 (center: 513.6)
    # NO box: X=529.5 to 561.4 (center: 545.5)
    x_width = can.stringWidth('X', "Helvetica", 10)
    yes_x = 513.6 - (x_width / 2)
    no_x = 545.5 - (x_width / 2)

    # 4. Substitute employer? (Y=69.9)
    y_pos = convert_y(69.9) - 3
    if data['substitute_employer'] == 'Y':
        can.drawString(yes_x, y_pos, 'X')
    else:
        can.drawString(no_x, y_pos, 'X')

    # 5. Resulting learnership? (Y=110.5)
    y_pos = convert_y(110.5) - 3
    if data['resulting_learnership'] == 'Y':
        can.drawString(yes_x, y_pos, 'X')
    else:
        can.drawString(no_x, y_pos, 'X')

    # 6. Deduction allowable? (Y=169.9)
    y_pos = convert_y(169.9) - 3
    if data['deduction_allowable'] == 'Y':
        can.drawString(yes_x, y_pos, 'X')
    else:
        can.drawString(no_x, y_pos, 'X')

    can.save()
    packet.seek(0)
    return packet

def populate_pdf_for_row(row_data, template_path):
    """Populate PDF with data from a single row"""
    # Extract learner name and ID from separate columns
    learner_name = str(row_data['Full Names']) if pd.notna(row_data['Full Names']) else ''
    learner_id = str(row_data['ID Number']) if pd.notna(row_data['ID Number']) else ''

    data = {
        'tax_ref': str(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) if pd.notna(row_data['Inkomstebelastingverwysingsnommer van werkgewer']) else '',
        'year': str(int(row_data['Year of Assessment'])) if pd.notna(row_data['Year of Assessment']) else '',
        'employer_name': str(row_data['Geregistreerde naam van werkgewer']) if pd.notna(row_data['Geregistreerde naam van werkgewer']) else '',
        'sdl_ref': str(row_data['Skills Development Levy reference number']) if pd.notna(row_data['Skills Development Levy reference number']) else '',
        'seta_name': str(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) if pd.notna(row_data['Naam van SETA waar die leerlingooreenkoms geregistreer is']) else '',
        'learnership_title': str(row_data['Learnership Title']) if pd.notna(row_data['Learnership Title']) else '',
        'learnership_code': str(row_data['Learnership Code']) if pd.notna(row_data['Learnership Code']) else '',
        'learner_name': learner_name,
        'learner_id': learner_id,
        'start_date': row_data['Start date'],
        'end_date': row_data['End date'],
        'was_employed': str(row_data['Employed']) if pd.notna(row_data['Employed']) else 'N',
        'was_disabled': str(row_data['Disabled']) if pd.notna(row_data['Disabled']) else 'N',
        'in_trade': str(row_data['InTrade']) if pd.notna(row_data['InTrade']) else 'N',
        'substitute_employer': str(row_data['Substitute employer']) if pd.notna(row_data['Substitute employer']) else 'N',
        'resulting_learnership': str(row_data['Resulting Learningship']) if pd.notna(row_data['Resulting Learningship']) else 'N',
        'deduction_allowable': str(row_data['Deduction allowable']) if pd.notna(row_data['Deduction allowable']) else 'N',
        'representative_name': str(row_data['Representative']) if pd.notna(row_data['Representative']) else '',
        'period_months': int(row_data['Period']) if pd.notna(row_data['Period']) else 12,
        'annual_remuneration': float(row_data['Total Renumeration']) if pd.notna(row_data['Total Renumeration']) else 0.0,
        'deduction_claimed': float(row_data['Deduction Claimed']) if pd.notna(row_data['Deduction Claimed']) else 0.0,
        'limitation': float(row_data['Limit on Deduction']) if pd.notna(row_data['Limit on Deduction']) else 0.0,
    }

    overlay_packet = create_overlay(data)
    overlay_pdf = PdfReader(overlay_packet)

    # Create page 2 overlay with today's date and checkboxes
    page2_overlay_packet = create_page2_overlay(data)
    page2_overlay_pdf = PdfReader(page2_overlay_packet)

    original_pdf = PdfReader(template_path)
    writer = PdfWriter()

    # Merge page 1 with data overlay
    page = original_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])
    writer.add_page(page)

    # Merge page 2 with date overlay
    page2 = original_pdf.pages[1]
    page2.merge_page(page2_overlay_pdf.pages[0])
    writer.add_page(page2)

    # Add any remaining pages (if more than 2)
    for i in range(2, len(original_pdf.pages)):
        writer.add_page(original_pdf.pages[i])

    # Create PDF in memory
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)
    
    return output_buffer, learner_name, learner_id

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with detailed logging"""
    import traceback
    error_msg = str(error)
    traceback_str = traceback.format_exc()
    print(f"500 Error: {error_msg}")
    print(f"Traceback: {traceback_str}")
    return jsonify({'error': 'Internal server error. Please check the server logs for details.'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        import traceback
        print(f"Error rendering index: {str(e)}")
        print(traceback.format_exc())
        return f"Error loading page: {str(e)}", 500

@app.route('/test-logo')
def test_logo():
    """Test route to verify logo file is accessible"""
    import os
    logo_path = os.path.join(app.static_folder, 'logo.webp')
    if os.path.exists(logo_path):
        return send_file(logo_path, mimetype='image/webp')
    return "Logo file not found", 404

@app.route('/upload', methods=['POST'])
def upload_file():
    upload_path = None  # Track upload path for cleanup
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an Excel file (.xlsx or .xls)'}), 400

        # Check if template file exists
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
        
        if not os.path.exists(template_path):
            # Try Templates folder
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                        'Templates', 
                                        'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
            if not os.path.exists(template_path):
                return jsonify({'error': 'PDF template file not found. Please ensure the template PDF is in the project folder.'}), 500

        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Read Excel file
        try:
            df = pd.read_excel(upload_path)
        except Exception as e:
            # Clean up uploaded file on error
            if upload_path and os.path.exists(upload_path):
                try:
                    os.remove(upload_path)
                except:
                    pass
            return jsonify({'error': f'Error reading Excel file: {str(e)}'}), 400

        if len(df) == 0:
            # Clean up uploaded file on empty file error
            if upload_path and os.path.exists(upload_path):
                try:
                    os.remove(upload_path)
                except:
                    pass
            return jsonify({'error': 'Excel file is empty'}), 400

        # Validate required columns
        required_columns = [
            'Inkomstebelastingverwysingsnommer van werkgewer',
            'Year of Assessment',
            'Geregistreerde naam van werkgewer',
            'Skills Development Levy reference number',
            'Naam van SETA waar die leerlingooreenkoms geregistreer is',
            'Learnership Title',
            'Learnership Code',
            'Full Names',
            'ID Number',
            'Start date',
            'End date',
            'Employed',
            'Disabled',
            'InTrade',
            'Substitute employer',
            'Resulting Learningship',
            'Deduction allowable',
            'Period',
            'Total Renumeration',
            'Deduction Claimed',
            'Limit on Deduction',
            'Representative'
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            # Clean up uploaded file on validation error
            if upload_path and os.path.exists(upload_path):
                try:
                    os.remove(upload_path)
                except:
                    pass
            return jsonify({
                'error': f'Missing required columns: {", ".join(missing_columns)}',
                'missing_columns': missing_columns
            }), 400

        # Create output directory for this session
        session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
        os.makedirs(output_dir, exist_ok=True)

        # Process each row and generate PDFs
        successful = 0
        failed = 0
        errors = []

        for index, row in df.iterrows():
            try:
                pdf_buffer, learner_name, learner_id = populate_pdf_for_row(row, template_path)
                
                # Create safe filename
                safe_name = learner_name.replace(" ", "_") if learner_name else "Unknown"
                safe_id = str(learner_id).replace(" ", "_").replace("-", "") if learner_id else "NoID"
                output_filename = f'IT180_{safe_name}_{safe_id}.pdf'
                output_path = os.path.join(output_dir, output_filename)
                
                # Save PDF
                with open(output_path, 'wb') as f:
                    f.write(pdf_buffer.getvalue())
                
                successful += 1
            except Exception as e:
                failed += 1
                errors.append(f"Row {index + 1}: {str(e)}")

        # Create ZIP file with all PDFs
        zip_path = os.path.join(output_dir, 'IT180_Documents.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_file in os.listdir(output_dir):
                if pdf_file.endswith('.pdf'):
                    zipf.write(os.path.join(output_dir, pdf_file), pdf_file)

        # Clean up uploaded Excel file immediately after PDFs are created
        try:
            if os.path.exists(upload_path):
                os.remove(upload_path)
        except Exception as e:
            print(f"Warning: Could not delete uploaded file: {e}")

        return jsonify({
            'success': True,
            'message': f'Successfully processed {successful} rows',
            'total_rows': len(df),
            'successful': successful,
            'failed': failed,
            'errors': errors[:10],  # Limit to first 10 errors
            'download_url': f'/download/{session_id}',
            'zip_url': f'/download/{session_id}/zip'
        })

    except Exception as e:
        # Ensure uploaded file is cleaned up even on server error
        if upload_path and os.path.exists(upload_path):
            try:
                os.remove(upload_path)
            except:
                pass
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def cleanup_session_files(output_dir):
    """Clean up all files in a session directory after download"""
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
    except Exception as e:
        print(f"Warning: Could not clean up session files: {e}")

@app.route('/download/<session_id>')
def download_pdfs(session_id):
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
    if not os.path.exists(output_dir):
        return "Session not found", 404
    
    # List all PDFs
    pdf_files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
    if not pdf_files:
        return "No PDFs found", 404
    
    # Schedule cleanup after response is sent
    @after_this_request
    def cleanup_after_download(response):
        # Use a background thread to clean up after a short delay
        # This ensures the file is fully sent before deletion
        def delayed_cleanup():
            time.sleep(2)  # Wait 2 seconds to ensure download completes
            cleanup_session_files(output_dir)
        
        thread = threading.Thread(target=delayed_cleanup)
        thread.daemon = True
        thread.start()
        return response
    
    # If only one PDF, return it directly
    if len(pdf_files) == 1:
        return send_file(
            os.path.join(output_dir, pdf_files[0]),
            as_attachment=True,
            download_name=pdf_files[0]
        )
    
    # Otherwise, return ZIP
    zip_path = os.path.join(output_dir, 'IT180_Documents.zip')
    if os.path.exists(zip_path):
        return send_file(
            zip_path,
            as_attachment=True,
            download_name='IT180_Documents.zip'
        )
    
    return "Files not found", 404

@app.route('/download/<session_id>/zip')
def download_zip(session_id):
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
    zip_path = os.path.join(output_dir, 'IT180_Documents.zip')
    
    if not os.path.exists(zip_path):
        return "ZIP file not found", 404
    
    # Schedule cleanup after response is sent
    @after_this_request
    def cleanup_after_download(response):
        # Use a background thread to clean up after a short delay
        # This ensures the file is fully sent before deletion
        def delayed_cleanup():
            time.sleep(2)  # Wait 2 seconds to ensure download completes
            cleanup_session_files(output_dir)
        
        thread = threading.Thread(target=delayed_cleanup)
        thread.daemon = True
        thread.start()
        return response
    
    return send_file(
        zip_path,
        as_attachment=True,
        download_name='IT180_Documents.zip'
    )

if __name__ == '__main__':
    # Clean up old temp directories on startup
    try:
        for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not clean up temp directories: {e}")
    
    # Verify template file exists
    template_paths = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                    'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                    'Templates', 
                    'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf')
    ]
    template_found = any(os.path.exists(path) for path in template_paths)
    if not template_found:
        print("WARNING: PDF template file not found. The application may not work correctly.")
    else:
        print("✓ PDF template file found")
    
    # Verify template HTML exists
    template_html = os.path.join(app.template_folder, 'index.html')
    if os.path.exists(template_html):
        print("✓ HTML template found")
    else:
        print(f"WARNING: HTML template not found at {template_html}")
    
    # Get port from environment variable (for cloud deployment) or use 5000
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("Starting IT180 PDF Generator Web Application...")
    print(f"Server running on port {port}")
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    app.run(debug=debug, host='0.0.0.0', port=port)
