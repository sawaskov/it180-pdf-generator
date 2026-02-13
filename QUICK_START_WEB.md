# Quick Start - Web Application

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 📤 How to Use

1. **Upload** your Excel file (.xlsx or .xls)
2. **Wait** for processing (progress bar will show status)
3. **Download** the ZIP file containing all PDFs

That's it! 🎉

## 📋 Requirements

Your Excel file must have all required columns. See the web interface for a complete list, or check `WEB_APP_GUIDE.md` for details.

## ❓ Troubleshooting

**Can't install dependencies?**
- Make sure Python 3.x is installed
- Try: `python -m pip install -r requirements.txt`

**Template PDF not found?**
- Ensure `IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf` exists in:
  - The main project folder, OR
  - The `Templates/` folder

**Port 5000 already in use?**
- Edit `app.py` and change `port=5000` to a different port (e.g., `port=5001`)
- Then access: `http://localhost:5001`

For more details, see **WEB_APP_GUIDE.md**
