const { PDFDocument, rgb, StandardFonts } = require('pdf-lib');
const fs = require('fs-extra');
const path = require('path');
const ExcelJS = require('exceljs');
const archiver = require('archiver');

// A4 page dimensions in points
const PAGE_WIDTH = 595.27;
const PAGE_HEIGHT = 841.89;

/**
 * Clean text for PDF - remove special characters and normalize whitespace
 */
function cleanText(text) {
  if (!text || text === 'null' || text === 'undefined' || text === 'NaN') {
    return '';
  }
  const str = String(text);
  // Replace tabs with spaces
  let cleaned = str.replace(/\t/g, ' ');
  // Replace multiple spaces with single space
  cleaned = cleaned.replace(/\s+/g, ' ');
  // Remove control characters except newlines
  cleaned = cleaned.replace(/[\x00-\x1F\x7F]/g, '');
  // Strip leading/trailing whitespace
  return cleaned.trim();
}

/**
 * Convert Y coordinate from top-origin to bottom-origin (PDF coordinate system)
 */
function convertY(yFromTop) {
  return PAGE_HEIGHT - yFromTop;
}

/**
 * Create overlay PDF for page 1 with all form fields
 */
async function createPage1Overlay(data) {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([PAGE_WIDTH, PAGE_HEIGHT]);
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
  const fontSize = 9;
  const fontSizeLarge = 10;

  // Helper function to draw text
  const drawText = (text, x, y, size = fontSize, align = 'left') => {
    if (!text) return;
    const cleaned = cleanText(text);
    if (!cleaned) return;
    
    page.drawText(cleaned, {
      x: x,
      y: y,
      size: size,
      font: font,
    });
  };

  // Helper to center text in a box
  const drawCenteredText = (text, centerX, y, size = fontSize) => {
    if (!text) return;
    const cleaned = String(text);
    const textWidth = font.widthOfTextAtSize(cleaned, size);
    const x = centerX - (textWidth / 2);
    drawText(cleaned, x, y, size);
  };

  // ===== TAX REFERENCE NUMBER (10 boxes) =====
  const taxRef = String(data.tax_ref || '').padStart(10, '0').substring(0, 10);
  const xStart = 348;
  const yPos = convertY(182);
  const boxWidth = 14.17;
  for (let i = 0; i < taxRef.length; i++) {
    drawText(taxRef[i], xStart + (i * boxWidth), yPos);
  }

  // ===== YEAR OF ASSESSMENT (4 boxes) =====
  const year = String(data.year || '');
  const boxesX = [433, 447, 461, 475];
  const yearY = convertY(202);
  for (let i = 0; i < Math.min(year.length, 4); i++) {
    drawText(year[i], boxesX[i], yearY);
  }

  // ===== REGISTERED NAME OF EMPLOYER (text field) =====
  drawText(data.employer_name || '', 40, convertY(296.7) - 3);

  // ===== SDL REFERENCE NUMBER (boxes after L) =====
  const sdlRef = String(data.sdl_ref || '').replace('L', '').trim();
  const sdlBoxesX = [440.4, 454.6, 468.8, 482.9, 497.1, 511.3, 525.5, 539.6, 553.8];
  const sdlY = convertY(333.3) - 3;
  for (let i = 0; i < Math.min(sdlRef.length, 9); i++) {
    drawCenteredText(sdlRef[i], sdlBoxesX[i], sdlY);
  }

  // ===== NAME OF SETA (text field) =====
  drawText(data.seta_name || '', 40, convertY(373.0) - 3);

  // ===== LEARNERSHIP TITLE (text field) =====
  if (data.learnership_title && String(data.learnership_title) !== 'nan') {
    drawText(data.learnership_title, 40, convertY(443.0) - 3);
  }

  // ===== LEARNERSHIP CODE (text field) =====
  if (data.learnership_code && String(data.learnership_code) !== 'nan') {
    drawText(data.learnership_code, 40, convertY(458.9) - 3);
  }

  // ===== LEARNER FULL NAME (text field) =====
  drawText(data.learner_name || '', 40, convertY(494.7) - 3);

  // ===== ID NUMBER (13 boxes) =====
  if (data.learner_id) {
    const idNum = String(data.learner_id).replace(/[-\s]/g, '').substring(0, 13);
    const idXStart = 38;
    const idY = convertY(513);
    const idBoxWidth = 14.17;
    for (let i = 0; i < idNum.length; i++) {
      drawText(idNum[i], idXStart + (i * idBoxWidth), idY);
    }
  }

  // ===== START DATE (CCYY-MM-DD in boxes) =====
  if (data.start_date) {
    let dateStr;
    if (data.start_date instanceof Date) {
      dateStr = data.start_date.toISOString().replace(/[-:T]/g, '').substring(0, 8);
    } else {
      // Try to parse as date string
      const date = new Date(data.start_date);
      if (!isNaN(date.getTime())) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        dateStr = `${year}${month}${day}`;
      }
    }
    
    if (dateStr) {
      const dateY = convertY(532.1) - 3;
      
      // CCYY: 4 digits
      const ccyyX = [446.2, 458.2, 470.1, 482.1];
      for (let i = 0; i < 4; i++) {
        drawCenteredText(dateStr[i], ccyyX[i], dateY);
      }
      
      // MM: 2 digits
      const mmX = [506.6, 518.6];
      for (let i = 0; i < 2; i++) {
        drawCenteredText(dateStr[4 + i], mmX[i], dateY);
      }
      
      // DD: 2 digits
      const ddX = [542.8, 554.8];
      for (let i = 0; i < 2; i++) {
        drawCenteredText(dateStr[6 + i], ddX[i], dateY);
      }
    }
  }

  // ===== END DATE (CCYY-MM-DD in boxes) =====
  if (data.end_date) {
    let dateStr;
    if (data.end_date instanceof Date) {
      dateStr = data.end_date.toISOString().replace(/[-:T]/g, '').substring(0, 8);
    } else {
      const date = new Date(data.end_date);
      if (!isNaN(date.getTime())) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        dateStr = `${year}${month}${day}`;
      }
    }
    
    if (dateStr) {
      const dateY = convertY(562.7) - 3;
      
      // CCYY: 4 digits
      const ccyyX = [446.2, 458.2, 470.1, 482.1];
      for (let i = 0; i < 4; i++) {
        drawCenteredText(dateStr[i], ccyyX[i], dateY);
      }
      
      // MM: 2 digits
      const mmX = [506.6, 518.6];
      for (let i = 0; i < 2; i++) {
        drawCenteredText(dateStr[4 + i], mmX[i], dateY);
      }
      
      // DD: 2 digits
      const ddX = [542.8, 554.8];
      for (let i = 0; i < 2; i++) {
        drawCenteredText(dateStr[6 + i], ddX[i], dateY);
      }
    }
  }

  // ===== CHECKBOXES ON PAGE 1 =====
  const xWidth = font.widthOfTextAtSize('X', fontSizeLarge);
  const yesX = 513.6 - (xWidth / 2);
  const noX = 545.5 - (xWidth / 2);

  // 1. Was employed? (Y=602.5)
  let checkboxY = convertY(602.5) - 3;
  drawText(data.was_employed === 'Y' ? 'X' : 'X', data.was_employed === 'Y' ? yesX : noX, checkboxY, fontSizeLarge);

  // 2. Was disabled? (Y=628.3)
  checkboxY = convertY(628.3) - 3;
  drawText(data.was_disabled === 'Y' ? 'X' : 'X', data.was_disabled === 'Y' ? yesX : noX, checkboxY, fontSizeLarge);

  // 3. In course of trade? (Y=654.2)
  checkboxY = convertY(654.2) - 3;
  drawText(data.in_trade === 'Y' ? 'X' : 'X', data.in_trade === 'Y' ? yesX : noX, checkboxY, fontSizeLarge);

  // ===== PERIOD (MONTHS) - 2 boxes =====
  const months = String(data.period_months || 12).padStart(2, '0');
  const periodBoxesX = [183, 197];
  const periodY = convertY(684);
  for (let i = 0; i < Math.min(months.length, 2); i++) {
    drawText(months[i], periodBoxesX[i], periodY);
  }

  // ===== ANNUAL REMUNERATION (R boxes - 7 visible boxes) =====
  if (data.annual_remuneration > 0) {
    const remuneration = String(Math.floor(data.annual_remuneration));
    const remBoxesX = [414, 430, 442, 455, 470, 483, 496];
    const remY = convertY(740);
    // Start from the rightmost box and work backwards
    for (let i = 0; i < remuneration.length; i++) {
      const digitPos = remuneration.length - 1 - i;
      const boxPos = 6 - i;
      if (boxPos >= 0) {
        drawText(remuneration[digitPos], remBoxesX[boxPos], remY);
      }
    }
  }

  // ===== DEDUCTION CLAIMED (R boxes - 7 visible boxes) =====
  if (data.deduction_claimed > 0) {
    const deduction = String(Math.floor(data.deduction_claimed));
    const dedBoxesX = [414, 430, 442, 455, 470, 483, 496];
    const dedY = convertY(764);
    for (let i = 0; i < deduction.length; i++) {
      const digitPos = deduction.length - 1 - i;
      const boxPos = 6 - i;
      if (boxPos >= 0) {
        drawText(deduction[digitPos], dedBoxesX[boxPos], dedY);
      }
    }
  }

  // ===== LIMITATION (R boxes - 7 visible boxes) =====
  if (data.limitation > 0) {
    const limitation = String(Math.floor(data.limitation));
    const limBoxesX = [414, 430, 442, 455, 470, 483, 496];
    const limY = convertY(788);
    for (let i = 0; i < limitation.length; i++) {
      const digitPos = limitation.length - 1 - i;
      const boxPos = 6 - i;
      if (boxPos >= 0) {
        drawText(limitation[digitPos], limBoxesX[boxPos], limY);
      }
    }
  }

  const pdfBytes = await pdfDoc.save();
  return pdfBytes;
}

/**
 * Create overlay PDF for page 2 with today's date and checkboxes
 */
async function createPage2Overlay(data) {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([PAGE_WIDTH, PAGE_HEIGHT]);
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
  const fontSize = 9;
  const fontSizeLarge = 10;

  const drawText = (text, x, y, size = fontSize) => {
    if (!text) return;
    const cleaned = cleanText(text);
    if (!cleaned) return;
    page.drawText(cleaned, { x, y, size, font });
  };

  const drawCenteredText = (text, centerX, y, size = fontSize) => {
    if (!text) return;
    const cleaned = String(text);
    const textWidth = font.widthOfTextAtSize(cleaned, size);
    const x = centerX - (textWidth / 2);
    drawText(cleaned, x, y, size);
  };

  // ===== REPRESENTATIVE NAME (text field on page 2) =====
  if (data.representative_name) {
    drawText(data.representative_name, 45, convertY(204.1) - 3);
  }

  // Get today's date
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  const dateStr = `${year}${month}${day}`;

  // Date boxes on page 2 at Y=261.7
  const dateY = convertY(261.7) - 3;

  // CCYY: 4 digits
  const ccyyStart = 440.2;
  const ccyyWidth = 47.9;
  const digitWidth = ccyyWidth / 4;
  const ccyyX = [];
  for (let i = 0; i < 4; i++) {
    ccyyX.push(ccyyStart + (i * digitWidth) + (digitWidth / 2));
  }

  for (let i = 0; i < 4; i++) {
    drawCenteredText(dateStr[i], ccyyX[i], dateY);
  }

  // MM: 2 digits
  const mmStart = 500.6;
  const mmWidth = 24.0;
  const mmDigitWidth = mmWidth / 2;
  const mmX = [];
  for (let i = 0; i < 2; i++) {
    mmX.push(mmStart + (i * mmDigitWidth) + (mmDigitWidth / 2));
  }

  for (let i = 0; i < 2; i++) {
    drawCenteredText(dateStr[4 + i], mmX[i], dateY);
  }

  // DD: 2 digits
  const ddStart = 536.8;
  const ddWidth = 24.0;
  const ddDigitWidth = ddWidth / 2;
  const ddX = [];
  for (let i = 0; i < 2; i++) {
    ddX.push(ddStart + (i * ddDigitWidth) + (ddDigitWidth / 2));
  }

  for (let i = 0; i < 2; i++) {
    drawCenteredText(dateStr[6 + i], ddX[i], dateY);
  }

  // ===== CHECKBOXES ON PAGE 2 =====
  const xWidth = font.widthOfTextAtSize('X', fontSizeLarge);
  const yesX = 513.6 - (xWidth / 2);
  const noX = 545.5 - (xWidth / 2);

  // 4. Substitute employer? (Y=69.9)
  let checkboxY = convertY(69.9) - 3;
  drawText('X', data.substitute_employer === 'Y' ? yesX : noX, checkboxY, fontSizeLarge);

  // 5. Resulting learnership? (Y=110.5)
  checkboxY = convertY(110.5) - 3;
  drawText('X', data.resulting_learnership === 'Y' ? yesX : noX, checkboxY, fontSizeLarge);

  // 6. Deduction allowable? (Y=169.9)
  checkboxY = convertY(169.9) - 3;
  drawText('X', data.deduction_allowable === 'Y' ? yesX : noX, checkboxY, fontSizeLarge);

  const pdfBytes = await pdfDoc.save();
  return pdfBytes;
}

/**
 * Populate PDF with data from a single row
 */
async function populatePdfForRow(rowData, templatePath) {
  // Extract learner name and ID
  const learnerName = rowData['Full Names'] ? String(rowData['Full Names']) : '';
  const learnerId = rowData['ID Number'] ? String(rowData['ID Number']) : '';

  // Prepare data object
  const data = {
    tax_ref: rowData['Inkomstebelastingverwysingsnommer van werkgewer'] 
      ? String(rowData['Inkomstebelastingverwysingsnommer van werkgewer']) : '',
    year: rowData['Year of Assessment'] 
      ? String(Math.floor(rowData['Year of Assessment'])) : '',
    employer_name: rowData['Geregistreerde naam van werkgewer'] 
      ? String(rowData['Geregistreerde naam van werkgewer']) : '',
    sdl_ref: rowData['Skills Development Levy reference number'] 
      ? String(rowData['Skills Development Levy reference number']) : '',
    seta_name: rowData['Naam van SETA waar die leerlingooreenkoms geregistreer is'] 
      ? String(rowData['Naam van SETA waar die leerlingooreenkoms geregistreer is']) : '',
    learnership_title: rowData['Learnership Title'] 
      ? String(rowData['Learnership Title']) : '',
    learnership_code: rowData['Learnership Code'] 
      ? String(rowData['Learnership Code']) : '',
    learner_name: learnerName,
    learner_id: learnerId,
    start_date: rowData['Start date'],
    end_date: rowData['End date'],
    was_employed: rowData['Employed'] ? String(rowData['Employed']) : 'N',
    was_disabled: rowData['Disabled'] ? String(rowData['Disabled']) : 'N',
    in_trade: rowData['InTrade'] ? String(rowData['InTrade']) : 'N',
    substitute_employer: rowData['Substitute employer'] 
      ? String(rowData['Substitute employer']) : 'N',
    resulting_learnership: rowData['Resulting Learningship'] 
      ? String(rowData['Resulting Learningship']) : 'N',
    deduction_allowable: rowData['Deduction allowable'] 
      ? String(rowData['Deduction allowable']) : 'N',
    representative_name: rowData['Representative'] 
      ? String(rowData['Representative']) : '',
    period_months: rowData['Period'] ? Math.floor(rowData['Period']) : 12,
    annual_remuneration: rowData['Total Renumeration'] 
      ? parseFloat(rowData['Total Renumeration']) : 0.0,
    deduction_claimed: rowData['Deduction Claimed'] 
      ? parseFloat(rowData['Deduction Claimed']) : 0.0,
    limitation: rowData['Limit on Deduction'] 
      ? parseFloat(rowData['Limit on Deduction']) : 0.0,
  };

  // Load template PDF
  const templateBytes = await fs.readFile(templatePath);
  const pdfDoc = await PDFDocument.load(templateBytes);

  // Create overlays
  const page1OverlayBytes = await createPage1Overlay(data);
  const page2OverlayBytes = await createPage2Overlay(data);

  // Load overlays as separate PDFs
  const page1OverlayDoc = await PDFDocument.load(page1OverlayBytes);
  const page2OverlayDoc = await PDFDocument.load(page2OverlayBytes);

  // Embed overlay PDFs - embedPdf returns an array of embedded pages
  const embeddedPage1Overlay = await pdfDoc.embedPdf(page1OverlayDoc);
  const embeddedPage2Overlay = await pdfDoc.embedPdf(page2OverlayDoc);

  // Merge page 1 - draw overlay on original page
  const originalPage1 = pdfDoc.getPage(0);
  originalPage1.drawPage(embeddedPage1Overlay[0]);

  // Merge page 2
  if (pdfDoc.getPageCount() > 1) {
    const originalPage2 = pdfDoc.getPage(1);
    originalPage2.drawPage(embeddedPage2Overlay[0]);
  }

  // Save PDF
  const pdfBytes = await pdfDoc.save();
  
  return { pdfBytes, learnerName, learnerId };
}

/**
 * Process Excel file and generate PDFs
 */
async function processExcelFile(excelPath, templatePath, outputDir) {
  // Read Excel file
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(excelPath);

  const worksheet = workbook.worksheets[0];
  if (!worksheet) {
    return { success: false, error: 'Excel file has no worksheets' };
  }

  // Validate required columns
  const requiredColumns = [
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
  ];

  const headers = [];
  worksheet.getRow(1).eachCell({ includeEmpty: false }, (cell, colNumber) => {
    headers[colNumber] = cell.value;
  });

  const missingColumns = requiredColumns.filter(col => !headers.includes(col));
  if (missingColumns.length > 0) {
    return {
      success: false,
      error: `Missing required columns: ${missingColumns.join(', ')}`,
      missing_columns: missingColumns
    };
  }

  // Create session directory
  const sessionId = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const sessionDir = path.join(outputDir, sessionId);
  await fs.ensureDir(sessionDir);

  // Process each row
  let successful = 0;
  let failed = 0;
  const errors = [];

  // Convert worksheet to row data
  const rows = [];
  worksheet.eachRow((row, rowNumber) => {
    if (rowNumber === 1) return; // Skip header row
    
    const rowData = {};
    row.eachCell({ includeEmpty: true }, (cell, colNumber) => {
      const header = headers[colNumber];
      if (header) {
        rowData[header] = cell.value;
      }
    });
    rows.push(rowData);
  });

  for (let index = 0; index < rows.length; index++) {
    const rowData = rows[index];
    try {
      const { pdfBytes, learnerName, learnerId } = await populatePdfForRow(rowData, templatePath);
      
      // Create safe filename
      const safeName = (learnerName || 'Unknown').replace(/[^a-zA-Z0-9]/g, '_');
      const safeId = (learnerId || 'NoID').replace(/[^a-zA-Z0-9]/g, '');
      const outputFilename = `IT180_${safeName}_${safeId}.pdf`;
      const outputPath = path.join(sessionDir, outputFilename);
      
      // Save PDF
      await fs.writeFile(outputPath, pdfBytes);
      
      successful++;
    } catch (error) {
      failed++;
      errors.push(`Row ${index + 2}: ${error.message}`);
    }
  }

  // Create ZIP file
  const zipPath = path.join(sessionDir, 'IT180_Documents.zip');
  await new Promise((resolve, reject) => {
    const output = fs.createWriteStream(zipPath);
    const archive = archiver('zip', { zlib: { level: 9 } });

    output.on('close', () => resolve());
    archive.on('error', (err) => reject(err));

    archive.pipe(output);

    // Add all PDF files to ZIP
    const files = fs.readdirSync(sessionDir).filter(f => f.endsWith('.pdf'));
    files.forEach(file => {
      archive.file(path.join(sessionDir, file), { name: file });
    });

    archive.finalize();
  });

  return {
    success: true,
    total_rows: rows.length,
    successful,
    failed,
    errors,
    sessionId
  };
}

module.exports = {
  processExcelFile,
  populatePdfForRow
};
