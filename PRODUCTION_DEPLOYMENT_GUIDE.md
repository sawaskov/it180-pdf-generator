# 🚀 Production Deployment Guide - Get Your Public URL

## Quick Start (5 Minutes)

### Option 1: Render.com (Recommended - FREE)

**Step 1: Prepare Code** ✅
- Your code is already ready!
- Run: `DEPLOY_TO_PRODUCTION.bat` to prepare

**Step 2: Create GitHub Repository**
1. Go to: https://github.com/new
2. Repository name: `it180-pdf-generator`
3. Make it **PUBLIC** (required for free Render.com)
4. Click "Create repository"
5. Copy the repository URL

**Step 3: Push Code to GitHub**
```bash
# If you haven't already, run:
git remote add origin YOUR_REPO_URL
git branch -M main
git push -u origin main
```

**Step 4: Deploy to Render.com**
1. Go to: https://render.com
2. Sign up (free) - use GitHub login for easiest setup
3. Click "New +" → "Web Service"
4. Connect GitHub → Select your repository
5. Configure:
   - **Name**: `it180-pdf-generator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free
6. (Optional) Add Environment Variable:
   - Key: `SECRET_KEY`
   - Value: Generate a random string (for security)
7. Click "Create Web Service"
8. Wait 2-5 minutes for deployment
9. **Get your public URL!** 🎉

Your app will be live at: `https://it180-pdf-generator.onrender.com`

---

## Option 2: Railway.app (Also Free & Easy)

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects everything!
6. Get your URL instantly

---

## Option 3: Replit (No Git Needed)

1. Go to: https://replit.com
2. Create new Python Repl
3. Upload all your project files
4. Run: `pip install -r requirements.txt`
5. Click "Run" button
6. Get public URL immediately!

---

## Automated Deployment Script

**Run this file:** `DEPLOY_TO_PRODUCTION.bat`

This script will:
- ✅ Verify all files are ready
- ✅ Set up Git repository
- ✅ Help you connect to GitHub
- ✅ Push your code
- ✅ Open Render.com for deployment

---

## What You'll Get

After deployment, you'll have:
- ✅ Public URL (e.g., `https://it180-pdf-generator.onrender.com`)
- ✅ Shareable link for your friends
- ✅ Free hosting (on Render.com free tier)
- ✅ Automatic HTTPS
- ✅ 24/7 availability

---

## Important Notes

### Free Tier Limitations (Render.com)
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (wake-up time)
- Perfect for personal/small team use

### To Keep App Always Awake (Optional)
- Upgrade to paid plan ($7/month)
- Or use a free "ping" service to keep it awake

### Security
- Set `SECRET_KEY` environment variable in production
- Don't commit sensitive data to GitHub

---

## Troubleshooting

**Deployment fails:**
- Check that all files are in GitHub repository
- Verify `requirements.txt` is correct
- Check build logs in Render dashboard

**App won't start:**
- Check logs in Render dashboard
- Verify Python version (should be 3.11+)
- Ensure all dependencies are in requirements.txt

**Can't access URL:**
- Wait a few minutes for deployment to complete
- Check deployment status in Render dashboard
- Verify the service is "Live" (not "Building")

---

## Need Help?

1. Check deployment logs in Render dashboard
2. Verify all files are in GitHub
3. Ensure requirements.txt includes all dependencies
4. Check that Procfile exists and is correct

---

**Ready to deploy?** Run `DEPLOY_TO_PRODUCTION.bat` now! 🚀
