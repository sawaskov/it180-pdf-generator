# Deploy to Render.com - Step by Step

## Quick Deploy (5 minutes)

### Step 1: Prepare Your Code
Your code is already prepared! All files are ready.

### Step 2: Create Render Account
1. Go to: https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest) or email

### Step 3: Deploy
1. Click "New +" button (top right)
2. Select "Web Service"
3. Connect your GitHub repository:
   - If you have the code on GitHub: Select your repo
   - If not: You'll need to push to GitHub first (see below)
4. Configure:
   - **Name**: `it180-pdf-generator` (or any name you like)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or `master`)
   - **Root Directory**: Leave blank (or `.` if needed)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free
5. Click "Create Web Service"

### Step 4: Wait for Deployment
- Render will build and deploy your app
- This takes 2-5 minutes
- You'll see build logs in real-time

### Step 5: Get Your URL
- Once deployed, you'll get a URL like:
  `https://it180-pdf-generator.onrender.com`
- This is your public URL!

## If You Don't Have GitHub

### Option A: Use Render's Manual Deploy
1. Create a ZIP of your project folder
2. Upload via Render's dashboard (if available)

### Option B: Push to GitHub First
1. Create account at github.com
2. Create new repository
3. Upload your files
4. Then follow Step 3 above

## Your Deployed URL Will Be:
`https://[your-app-name].onrender.com`

---

**That's it!** Your website will be live and accessible from anywhere.
