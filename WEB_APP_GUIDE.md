# IT180 PDF Generator - Web Application Guide

## Overview

The IT180 PDF Generator is now available as a web application! Upload your Excel file through a modern web interface and download all generated PDFs as a ZIP file.

## Quick Start

### 1. Install Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- pandas (Excel file reading)
- pypdf (PDF manipulation)
- reportlab (PDF generation)
- openpyxl (Excel file support)
- Werkzeug (Flask utilities)

### 2. Start the Web Server

Run the application:

```bash
python app.py
```

You should see:
```
Starting IT180 PDF Generator Web Application...
Open your browser and navigate to: http://localhost:5000
```

### 3. Access the Web Interface

Open your web browser and go to:
```
http://localhost:5000
```

## Using the Web Application

### Step 1: Upload Excel File

1. Click the "Choose File" button or drag and drop your Excel file onto the upload area
2. The file must be in `.xlsx` or `.xls` format
3. Ensure your Excel file has all required columns (see below)

### Step 2: Wait for Processing

- The application will process your Excel file
- A progress bar will show the processing status
- Processing time depends on the number of rows in your file

### Step 3: Download PDFs

- Once processing is complete, you'll see a summary:
  - Total rows processed
  - Number of successful PDFs
  - Number of failed PDFs (if any)
- Click the "Download PDFs (ZIP)" button to download all generated PDFs
- The ZIP file will contain all individual PDF files

## Excel File Requirements

Your Excel file must contain the following columns (exact names required):

### Basic Information
- `Inkomstebelastingverwysingsnommer van werkgewer` - Tax Reference Number
- `Year of Assessment` - Assessment Year
- `Geregistreerde naam van werkgewer` - Registered Employer Name
- `Skills Development Levy reference number` - SDL Reference Number (with L prefix)

### Learnership Details
- `Naam van SETA waar die leerlingooreenkoms geregistreer is` - SETA Name
- `Learnership Title` - Title of learnership
- `Learnership Code` - Learnership code

### Learner Information
- `Full Names` - Learner's full name
- `ID Number` - South African ID number
- `Start date` - Start date (Excel date format)
- `End date` - End date (Excel date format)

### Yes/No Flags (use Y or N)
- `Employed` - Was employed?
- `Disabled` - Was disabled?
- `InTrade` - In course of trade?
- `Substitute employer` - Substitute employer?
- `Resulting Learningship` - Resulting learnership?
- `Deduction allowable` - Deduction allowable?

### Financial & Other
- `Period` - Period in months
- `Total Renumeration` - Annual remuneration (optional, can be blank)
- `Deduction Claimed` - Deduction amount
- `Limit on Deduction` - Limitation amount
- `Representative` - Representative name

## Features

### Modern Web Interface
- Clean, user-friendly design
- Drag-and-drop file upload
- Real-time progress tracking
- Error handling and validation
- Responsive design (works on mobile devices)

### Automatic Processing
- Validates Excel file format
- Checks for required columns
- Generates PDFs for each row
- Creates ZIP file for easy download
- Shows detailed error messages if any rows fail

### Security
- File type validation
- Secure filename handling
- Temporary file cleanup
- Session-based file management

## Troubleshooting

### "No module named 'flask'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### "PDF template file not found"
**Solution:** Ensure the PDF template file exists in one of these locations:
- Main project folder: `IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf`
- Templates folder: `Templates/IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf`

### "Missing required columns" error
**Solution:** Check that your Excel file has all required columns with exact names (case-sensitive). See the column list above.

### File upload fails
**Solution:** 
- Check file size (max 50MB)
- Ensure file is `.xlsx` or `.xls` format
- Try a different browser
- Check browser console for errors

### PDFs not generating correctly
**Solution:**
- Verify all data in Excel is properly formatted
- Check that dates are in Excel date format
- Ensure Y/N fields contain only "Y" or "N"
- Review error messages in the results section

## Technical Details

### File Structure
```
SARS Pdf/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Web interface
├── static/
│   ├── style.css                  # Styling
│   └── script.js                  # Frontend JavaScript
├── IT180-Declaration...pdf        # PDF template (or in Templates/)
└── ...
```

### How It Works

1. **File Upload**: User uploads Excel file through web interface
2. **Validation**: Server validates file type and required columns
3. **Processing**: For each row:
   - Extracts data from Excel
   - Creates PDF overlay with positioned text
   - Merges with template PDF
   - Saves to temporary directory
4. **ZIP Creation**: All PDFs are packaged into a ZIP file
5. **Download**: User downloads the ZIP file
6. **Cleanup**: Temporary files are automatically cleaned up

### Server Configuration

The application runs on:
- **Host**: `0.0.0.0` (accessible from network)
- **Port**: `5000`
- **Debug Mode**: Enabled (for development)

To change these settings, edit the last line in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

For production, set `debug=False` and use a production WSGI server like Gunicorn.

## Production Deployment

For production use, consider:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set a secure secret key:**
   Change `app.secret_key` in `app.py` to a random string

3. **Configure proper file storage:**
   Update `UPLOAD_FOLDER` and `OUTPUT_FOLDER` paths

4. **Add authentication:**
   Implement user authentication if needed

5. **Use HTTPS:**
   Set up SSL/TLS certificates

## Support

For issues or questions:
1. Check the error messages in the web interface
2. Review the console output when running `app.py`
3. Verify your Excel file format matches the requirements
4. Check that the PDF template file is in the correct location

---

**Version:** 1.0 (Web Application)
**Last Updated:** 2025
