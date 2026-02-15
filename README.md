# IT180 PDF Form Generator

A Node.js/Express web application for generating IT180 tax forms from Excel data.

## Features

- Upload Excel files (.xlsx, .xls)
- Automatically generate IT180 PDF forms for each row
- Download all generated PDFs as a ZIP file
- Modern, responsive UI
- Real-time progress tracking

## Quick Start

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

### Production

```bash
npm start
```

The application will be available at `http://localhost:3000`

## Deployment

See `DEPLOY_NODEJS.md` for detailed deployment instructions.

Quick deploy: Run `DEPLOY_NOW_NODEJS.bat` for automated deployment assistance.

## Requirements

- Node.js 18.0.0 or higher
- npm 9.0.0 or higher

## Project Structure

```
├── server.js              # Express server
├── package.json           # Dependencies
├── views/                 # HTML templates
│   └── index.html
├── public/                # Static files
│   ├── style.css
│   ├── script.js
│   └── logo.webp
├── utils/                 # Utility functions
│   └── pdfGenerator.js
├── Templates/             # PDF template
│   └── IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf
└── temp/                  # Temporary file storage
```

## License

ISC
