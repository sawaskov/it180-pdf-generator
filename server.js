const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs-extra');
const { processExcelFile } = require('./utils/pdfGenerator');
const archiver = require('archiver');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/static', express.static(path.join(__dirname, 'public')));

// Configure multer for file uploads
const upload = multer({
  dest: path.join(__dirname, 'temp', 'uploads'),
  limits: {
    fileSize: 50 * 1024 * 1024 // 50MB max file size
  },
  fileFilter: (req, file, cb) => {
    const allowedExtensions = ['.xlsx', '.xls'];
    const fileExtension = path.extname(file.originalname).toLowerCase();
    if (allowedExtensions.includes(fileExtension)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Please upload an Excel file (.xlsx or .xls)'));
    }
  }
});

// Ensure temp directories exist
const tempDir = path.join(__dirname, 'temp');
const uploadDir = path.join(tempDir, 'uploads');
const outputDir = path.join(tempDir, 'output');

fs.ensureDirSync(uploadDir);
fs.ensureDirSync(outputDir);

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

app.post('/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file provided' });
    }

    // Check if template file exists
    let templatePath = path.join(__dirname, 'Templates', 
      'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf');
    
    if (!fs.existsSync(templatePath)) {
      // Try root directory
      const altTemplatePath = path.join(__dirname, 
        'IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf');
      if (!fs.existsSync(altTemplatePath)) {
        return res.status(500).json({ 
          error: 'PDF template file not found. Please ensure the template PDF is in the Templates folder.' 
        });
      }
      templatePath = altTemplatePath;
    }

    // Process the Excel file
    const result = await processExcelFile(req.file.path, templatePath, outputDir);

    // Clean up uploaded file
    await fs.remove(req.file.path);

    if (result.success) {
      res.json({
        success: true,
        message: `Successfully processed ${result.successful} rows`,
        total_rows: result.total_rows,
        successful: result.successful,
        failed: result.failed,
        errors: result.errors.slice(0, 10), // Limit to first 10 errors
        download_url: `/download/${result.sessionId}`,
        zip_url: `/download/${result.sessionId}/zip`
      });
    } else {
      res.status(400).json({
        success: false,
        error: result.error
      });
    }
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ error: `Server error: ${error.message}` });
  }
});

app.get('/download/:sessionId', (req, res) => {
  const sessionId = req.params.sessionId;
  const sessionDir = path.join(outputDir, sessionId);
  
  if (!fs.existsSync(sessionDir)) {
    return res.status(404).send('Session not found');
  }

  // List all PDFs
  const files = fs.readdirSync(sessionDir).filter(f => f.endsWith('.pdf'));
  if (files.length === 0) {
    return res.status(404).send('No PDFs found');
  }

  // If only one PDF, return it directly
  if (files.length === 1) {
    return res.download(
      path.join(sessionDir, files[0]),
      files[0]
    );
  }

  // Otherwise, return ZIP
  const zipPath = path.join(sessionDir, 'IT180_Documents.zip');
  if (fs.existsSync(zipPath)) {
    return res.download(zipPath, 'IT180_Documents.zip');
  }

  res.status(404).send('Files not found');
});

app.get('/download/:sessionId/zip', (req, res) => {
  const sessionId = req.params.sessionId;
  const sessionDir = path.join(outputDir, sessionId);
  const zipPath = path.join(sessionDir, 'IT180_Documents.zip');
  
  if (!fs.existsSync(zipPath)) {
    return res.status(404).send('ZIP file not found');
  }

  res.download(zipPath, 'IT180_Documents.zip');
});

// Error handling middleware
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({ error: 'File too large. Maximum size is 50MB.' });
    }
  }
  console.error(err);
  res.status(500).json({ error: err.message || 'Internal server error' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Starting IT180 PDF Generator Web Application...`);
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`Open your browser and navigate to: http://localhost:${PORT}`);
});
