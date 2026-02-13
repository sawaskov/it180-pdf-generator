# IT180 PDF Form Generator

Automated tool for generating IT180 tax forms from Excel data.

## Two Ways to Use

### 🌐 Web Application (Recommended)
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python app.py`
3. Open browser: `http://localhost:5000`
4. Upload Excel file and download PDFs

See **WEB_APP_GUIDE.md** for complete web app instructions.

### 💻 Command Line
1. Place your Excel file in the `Input` folder
2. Run the script: `python Scripts\fill_pdf_complete.py`
3. Find your PDFs in: `Output\IT180 Docs\`

See **USER_GUIDE.md** for complete command-line instructions.

## Folder Structure

- **app.py** - Web application (Flask)
- **templates/** - HTML templates for web interface
- **static/** - CSS and JavaScript files
- **Input/** - Place your Excel file here (command-line mode)
- **Output/** - Generated PDFs appear here (command-line mode)
- **Scripts/** - Command-line processing script
- **Templates/** - PDF template file
- **Archive/** - Old versions and test files

## Requirements

### For Web Application
- Python 3.x
- Flask, pandas, pypdf, reportlab, openpyxl

Install with: `pip install -r requirements.txt`

### For Command Line Only
- Python 3.x
- Libraries: pandas, pypdf, reportlab, openpyxl

Install with: `pip install pandas pypdf reportlab openpyxl`

## Support

For detailed instructions, troubleshooting, and Excel format requirements, see USER_GUIDE.md
