# Deployment Guide - IT180 PDF Generator

## Quick Deploy Options

### Option 1: Render.com (Recommended - Free Tier Available)

1. **Create a Render account**: Go to https://render.com and sign up (free)

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (or upload files)
   - Configure:
     - **Name**: it180-pdf-generator
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
     - **Plan**: Free

3. **Deploy**: Click "Create Web Service"
   - Your app will be available at: `https://it180-pdf-generator.onrender.com` (or your custom name)

### Option 2: Railway.app (Easy & Modern)

1. **Install Railway CLI** (optional, or use web interface):
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy via Web**:
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python and deploys

3. **Or Deploy via CLI**:
   ```bash
   railway init
   railway up
   ```

### Option 3: PythonAnywhere (Simple for Python)

1. **Sign up**: Go to https://www.pythonanywhere.com (free tier available)

2. **Upload files**:
   - Upload all project files via Files tab
   - Install dependencies in Bash console:
     ```bash
     pip3.10 install --user Flask pandas pypdf reportlab openpyxl Werkzeug
     ```

3. **Configure Web App**:
   - Go to Web tab
   - Create new web app
   - Set source code path
   - Set WSGI file to point to app.py

### Option 4: Replit (Very Easy)

1. **Go to**: https://replit.com
2. **Create new Repl**: Choose Python template
3. **Upload files**: Drag and drop all project files
4. **Install packages**: Run `pip install -r requirements.txt` in console
5. **Run**: Click Run button
6. **Get URL**: Replit provides a public URL automatically

## Important Notes for Deployment

### Template PDF File
Make sure the PDF template file is included in your deployment:
- `IT180-Declaration-by-Employer-to-Claim-Deduction-against-Learnerships-External-Form.pdf`
- Should be in root directory or `Templates/` folder

### Environment Variables (Optional)
For production, set these environment variables:
- `FLASK_ENV=production` (disables debug mode)
- `SECRET_KEY=your-secret-key-here` (change from default)

### File Size Limits
The app allows up to 50MB file uploads. Some free hosting services may have lower limits.

## Testing After Deployment

1. Visit your deployed URL
2. Upload a test Excel file
3. Verify PDFs are generated correctly
4. Test download functionality

## Troubleshooting

**App won't start:**
- Check that all dependencies are in requirements.txt
- Verify Python version compatibility
- Check logs for error messages

**Template PDF not found:**
- Ensure PDF file is in the repository
- Check file path in app.py matches deployment structure

**Upload fails:**
- Check file size limits on hosting service
- Verify CORS settings if needed
- Check server logs for specific errors

---

**Recommended**: Use Render.com for easiest deployment with free tier.
