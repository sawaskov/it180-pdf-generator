# IT180 PDF Form Generator - User Guide

## Table of Contents
1. [Overview](#overview)
2. [Folder Structure](#folder-structure)
3. [Prerequisites](#prerequisites)
4. [Step-by-Step Instructions](#step-by-step-instructions)
5. [Excel File Format Requirements](#excel-file-format-requirements)
6. [Troubleshooting](#troubleshooting)
7. [Technical Notes](#technical-notes)

---

## Overview

This tool automatically generates filled IT180 tax forms (Declaration by Employer to Claim Deduction against Learnerships) from an Excel spreadsheet. It processes learner data and creates individual PDF documents for each learner with all fields properly populated and positioned.

**What it does:**
- Reads learner data from an Excel file
- Populates IT180 PDF forms with accurate field positioning
- Generates one PDF per learner
- Saves all PDFs with unique filenames in an organized output folder

---

## Folder Structure

```
SARS Pdf/
├── Input/                          # Place your Excel file here
│   └── PEG 12H allowance - FY2025 (Clean).xlsx
│
├── Output/                         # Generated PDFs appear here
│   └── IT180 Docs/                # Individual PDF files
│
├── Scripts/                        # Main processing script
│   └── fill_pdf_complete.py      # The PDF generator script
│
├── Templates/                      # PDF template file
│   └── IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf
│
├── Archive/                        # Old versions and test files
│   └── (development files)
│
├── IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf
└── USER_GUIDE.md                  # This file
```

---

## Prerequisites

### Required Software
1. **Python 3.x** - Must be installed on your computer
2. **Required Python Libraries:**
   - pandas
   - pypdf
   - reportlab
   - openpyxl

### Installation Steps

1. **Check if Python is installed:**
   Open Command Prompt and type:
   ```
   python --version
   ```
   If Python is not installed, download from: https://www.python.org/downloads/

2. **Install required libraries:**
   Open Command Prompt and run:
   ```
   pip install pandas pypdf reportlab openpyxl
   ```

---

## Step-by-Step Instructions

### 1. Prepare Your Excel File

1. Open your Excel file containing learner data
2. Ensure all column names match exactly (see [Excel File Format Requirements](#excel-file-format-requirements))
3. Save the file as: `PEG 12H allowance - FY2025 (Clean).xlsx`
4. Place the file in the **Input** folder

### 2. Run the Script

**Method 1: Using Command Prompt**
1. Press `Windows + R`, type `cmd`, and press Enter
2. Navigate to the Scripts folder:
   ```
   cd "C:\Users\Speccon Admin\OneDrive\Desktop\SARS Pdf"
   ```
3. Run the script:
   ```
   python "Scripts\fill_pdf_complete.py"
   ```

**Method 2: Using File Explorer**
1. Navigate to: `C:\Users\Speccon Admin\OneDrive\Desktop\SARS Pdf\Scripts`
2. Right-click on `fill_pdf_complete.py`
3. Select "Open with" → "Python"

### 3. Monitor Progress

The script will display:
- Total number of rows found
- Progress updates every 10 rows
- Final summary showing successful and failed PDFs

Example output:
```
Found 388 rows in Excel file

Processing all 388 rows...
================================================================================
Processed 10/388 rows...
Processed 20/388 rows...
...
================================================================================

Processing complete!
Successfully created: 388 PDFs
```

### 4. Access Your PDFs

1. Navigate to: `Output\IT180 Docs\`
2. All generated PDFs will be there
3. Filename format: `IT180_{Learner_Name}_{ID_Number}.pdf`
   - Example: `IT180_Balintulo_Lisolethu_0105045541080.pdf`

---

## Excel File Format Requirements

### Required Column Names (Must match exactly)

| Column Name | Description | Example |
|------------|-------------|---------|
| `Inkomstebelastingverwysingsnommer van werkgewer` | Tax Reference Number | 7820714253 |
| `Year of Assessment` | Assessment Year | 2025 |
| `Geregistreerde naam van werkgewer` | Employer Name | BLOCKHOUSE ONE STOP (PTY) LTD |
| `Skills Development Levy reference number` | SDL Number with L prefix | L820714253 |
| `Naam van SETA waar die leerlingooreenkoms geregistreer is` | SETA Name | Services Seta |
| `Learnership Title` | Title of learnership | Generic Management NQF 3 |
| `Learnership Code` | Learnership code | 23Q230027371203 |
| `Full Names` | Learner full name | Balintulo Lisolethu |
| `ID Number` | South African ID | 0105045541080 |
| `Start date` | Start date | 2024-03-01 |
| `End date` | End date | 2025-02-28 |
| `Employed` | Was employed? | Y or N |
| `Disabled` | Was disabled? | Y or N |
| `InTrade` | In course of trade? | Y or N |
| `Substitute employer` | Substitute employer? | Y or N |
| `Resulting Learningship` | Resulting learnership? | Y or N |
| `Deduction allowable` | Deduction allowable? | Y or N |
| `Period` | Period in months | 12 |
| `Total Renumeration` | Annual remuneration (optional) | 56667 or blank |
| `Deduction Claimed` | Deduction amount | 56666.67 |
| `Limit on Deduction` | Limitation amount | 80000 |
| `Representative` | Representative name | Reinette Heyneke |

### Important Notes

1. **Column names must match exactly** - including capitalization and spelling
2. **Date format:** Excel date format (will be auto-converted)
3. **Y/N fields:** Use only "Y" or "N" (uppercase)
4. **Blank fields:** Leave blank if no value (especially for Total Renumeration)
5. **ID Numbers:** Can include or exclude spaces/dashes
6. **Special characters:** Tabs and special characters will be automatically cleaned

---

## Troubleshooting

### Problem: "No module named 'pandas'" (or pypdf, reportlab)
**Solution:** Install the missing library:
```
pip install pandas pypdf reportlab openpyxl
```

### Problem: "File not found" error
**Solution:**
- Check that your Excel file is named exactly: `PEG 12H allowance - FY2025 (Clean).xlsx`
- Ensure it's in the `Input` folder
- Check that the PDF template exists in the main folder

### Problem: Script runs but creates 0 PDFs
**Solution:**
- Verify Excel column names match exactly (see table above)
- Check that the Excel file contains data rows
- Ensure you're running from the correct directory

### Problem: Some fields appear blank on PDF
**Solution:**
- Check the Excel file has data in those columns
- Verify column names are spelled correctly
- Check for hidden characters or tabs in the data

### Problem: Duplicate learner names
**Solution:**
- This is handled automatically - PDFs now include ID numbers in filenames
- Example: Both "Medledle Athabile" learners will have separate PDFs with their unique IDs

### Problem: Missing PDFs for some rows
**Solution:**
- Check the console output for error messages
- Verify those rows have valid Full Names and ID Numbers
- Ensure no special characters in names that would make invalid filenames

---

## Technical Notes

### What the Script Does

1. **Reads Excel Data:** Loads the clean Excel file from the Input folder
2. **Processes Each Row:** Iterates through all learner records
3. **Creates PDF Overlay:** For each learner:
   - Generates a transparent overlay with filled-in text
   - Positions all fields accurately using coordinates
   - Handles checkboxes, dates, and amount fields
4. **Merges with Template:** Overlays data onto the blank IT180 form
5. **Saves Individual PDFs:** Creates unique files in Output folder

### Field Positioning Details

All fields are precisely positioned using PDF coordinates:
- **Text fields:** Centered vertically in white blocks
- **Number boxes:** Each digit centered in individual boxes
- **Checkboxes:** X marks centered in YES/NO boxes
- **Dates:** Formatted as CCYY-MM-DD in separate boxes
- **Amounts:** Right-aligned with no leading zeros

### Text Cleaning

The script automatically:
- Replaces tabs with spaces
- Removes control characters
- Normalizes multiple spaces to single space
- Strips leading/trailing whitespace

### Date Handling

- **Page 1:** Uses Start date and End date from Excel
- **Page 2:** Automatically uses today's date (when PDF is generated)

### Empty Fields

- If `Total Renumeration` is blank or 0, the field is left empty
- Same for `Deduction Claimed` and `Limit on Deduction`
- This prevents showing "0000000" in empty fields

---

## Quick Reference

### To Generate PDFs:
1. Place Excel file in `Input` folder
2. Run: `python "Scripts\fill_pdf_complete.py"`
3. Find PDFs in: `Output\IT180 Docs\`

### File Locations:
- **Input data:** `Input\PEG 12H allowance - FY2025 (Clean).xlsx`
- **Main script:** `Scripts\fill_pdf_complete.py`
- **Output PDFs:** `Output\IT180 Docs\`
- **Template:** `Templates\IT180-Declaration-by-Employer...pdf`

### Need Help?
- Check this guide's [Troubleshooting](#troubleshooting) section
- Verify [Excel File Format Requirements](#excel-file-format-requirements)
- Review console error messages for specific issues

---

**Version:** 1.0
**Last Updated:** October 2025
**Generated PDFs:** 388 (as of last run)
