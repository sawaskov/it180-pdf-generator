# 🚀 Quick Deployment Guide - Get Your App Live in 10 Minutes!

## Option 1: Render.com (Recommended - FREE & Easy)

### Step 1: Prepare Your Code
✅ Your code is already ready! All files are prepared for deployment.

### Step 2: Push to GitHub (If Not Already Done)

1. **If you don't have a GitHub account:**
   - Go to https://github.com and sign up (free)

2. **Create a new repository:**
   - Click "New" or "+" → "New repository"
   - Name it: `it180-pdf-generator` (or any name)
   - Make it **Public** (free tier on Render requires public repos)
   - Click "Create repository"

3. **Push your code to GitHub:**
   ```bash
   # In your project folder, run these commands:
   git init
   git add .
   git commit -m "Initial commit - IT180 PDF Generator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/it180-pdf-generator.git
   git push -u origin main
   ```
   (Replace YOUR_USERNAME with your GitHub username)

### Step 3: Deploy to Render.com

1. **Go to Render.com:**
   - Visit: https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (easiest option)

2. **Create New Web Service:**
   - Click "New +" button (top right)
   - Select "Web Service"
   - Connect your GitHub account if prompted
   - Select your repository: `it180-pdf-generator`

3. **Configure Your Service:**
   - **Name**: `it180-pdf-generator` (or any name you like)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

4. **Add Environment Variables (Optional but Recommended):**
   - Click "Advanced" → "Add Environment Variable"
   - Key: `SECRET_KEY`
   - Value: Generate a random string (you can use: https://randomkeygen.com/)
   - Click "Add"

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Watch the build logs

### Step 4: Get Your URL! 🎉

Once deployed, you'll get a URL like:
**`https://it180-pdf-generator.onrender.com`**

This is your public URL - share it with your friends!

---

## Option 2: Railway.app (Alternative - Also Free)

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects everything and deploys!
6. Get your URL from the dashboard

---

## Option 3: Replit (Easiest - No Git Needed)

1. Go to: https://replit.com
2. Sign up (free)
3. Click "Create Repl" → Choose "Python" template
4. Upload all your project files (drag and drop)
5. In the console, run: `pip install -r requirements.txt`
6. Click "Run" button
7. Replit gives you a public URL automatically!

---

## After Deployment - Test Your App

1. Visit your deployed URL
2. Upload a test Excel file
3. Verify PDFs are generated
4. Test the download functionality
5. Share the URL with your friends! 🎊

---

## Troubleshooting

**App won't start:**
- Check build logs in Render dashboard
- Verify all files are in the repository
- Make sure `requirements.txt` is correct

**Template PDF not found:**
- Ensure the PDF file is in your GitHub repository
- Check that `.gitignore` allows the template PDF

**Logo not showing:**
- Verify `static/logo.webp` is in the repository
- Clear browser cache after deployment

---

## Security Note

For production, make sure to:
- Set a strong `SECRET_KEY` environment variable
- Don't share your secret key publicly
- The app is configured to use environment variables automatically

---

**Need Help?** Check the full deployment guide in `DEPLOYMENT_GUIDE.md`
