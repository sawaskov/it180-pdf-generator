# 🚀 Node.js Production Deployment Guide

## Quick Start - Deploy to Render.com (Recommended - FREE)

### Step 1: Prepare Your Code

Your code is already ready! Just make sure you have:
- ✅ `package.json` with all dependencies
- ✅ `server.js` as the main entry point
- ✅ `Procfile` (already created)
- ✅ `.gitignore` (already created)

### Step 2: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: `it180-pdf-generator-nodejs`
3. Make it **PUBLIC** (required for free Render.com)
4. Click "Create repository"
5. Copy the repository URL

### Step 3: Push Code to GitHub

Open PowerShell in your project directory and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Node.js IT180 PDF Generator"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/it180-pdf-generator-nodejs.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Render.com

1. **Go to Render.com**: https://render.com
2. **Sign up** (free) - use GitHub login for easiest setup
3. **Click "New +"** → **"Web Service"**
4. **Connect GitHub** → Select your repository (`it180-pdf-generator-nodejs`)
5. **Configure settings**:
   - **Name**: `it180-pdf-generator`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Plan**: `Free`
6. **Click "Create Web Service"**
7. **Wait 2-5 minutes** for deployment
8. **Get your public URL!** 🎉

Your app will be live at: `https://it180-pdf-generator.onrender.com`

---

## Alternative: Railway.app (Also Free & Easy)

1. Go to: https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Node.js!
6. Get your URL instantly

**Railway auto-detects:**
- Node.js runtime
- `package.json` dependencies
- Start command from `package.json`

---

## Alternative: Vercel (Great for Node.js)

1. Go to: https://vercel.com
2. Sign up with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Vercel auto-detects Node.js
6. Click "Deploy"
7. Get your URL instantly!

---

## What You'll Get

After deployment, you'll have:
- ✅ Public URL (e.g., `https://it180-pdf-generator.onrender.com`)
- ✅ Shareable link
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
- Or use a free "ping" service (e.g., UptimeRobot) to keep it awake

### Environment Variables (Optional)
You can add these in Render.com dashboard under "Environment":
- `NODE_ENV=production`
- `PORT=3000` (automatically set by Render)

---

## Troubleshooting

**Deployment fails:**
- Check that all files are in GitHub repository
- Verify `package.json` is correct
- Check build logs in Render dashboard
- Ensure `server.js` exists and is the entry point

**App won't start:**
- Check logs in Render dashboard
- Verify Node.js version (Render uses latest LTS)
- Ensure all dependencies are in `package.json`
- Check that `Procfile` exists

**Can't access URL:**
- Wait a few minutes for deployment to complete
- Check deployment status in Render dashboard
- Verify the service is "Live" (not "Building")

**File upload issues:**
- Check that `temp/` directory permissions are correct
- Verify file size limits (50MB max)
- Check server logs for specific errors

---

## Production Checklist

Before deploying, ensure:
- [x] All dependencies in `package.json`
- [x] `Procfile` exists
- [x] `.gitignore` excludes `node_modules/` and `temp/`
- [x] PDF template file is in `Templates/` folder
- [x] Server uses `process.env.PORT` (already done)
- [x] Error handling is in place

---

## Quick Deploy Commands

**For Render.com:**
```bash
# After pushing to GitHub, just:
# 1. Go to render.com
# 2. Connect GitHub repo
# 3. Deploy!
```

**For Railway:**
```bash
# Railway auto-detects everything!
# Just connect GitHub and deploy
```

---

**Ready to deploy?** Follow Step 1-4 above! 🚀
