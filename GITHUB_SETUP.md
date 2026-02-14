# GitHub Repository Setup Guide

Your local git repository is ready with all your code committed! Now you need to:

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name**: `it180-pdf-generator` (or any name you prefer)
   - **Visibility**: Choose **Public** (required for free Render.com deployment) or **Private**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your project directory:

### Option A: If you just created the repository (no commits on GitHub yet)

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Option B: If you already have a repository with commits

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git pull origin main --allow-unrelated-histories
git push -u origin main
```

## Step 3: Replace YOUR_USERNAME and YOUR_REPO_NAME

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with the repository name you created

For example, if your username is `johndoe` and repo is `it180-pdf-generator`:
```bash
git remote add origin https://github.com/johndoe/it180-pdf-generator.git
```

## Quick Setup Script

You can also run the `setup_github.bat` file in this directory, which will guide you through the process interactively.

## After Pushing to GitHub

Once your code is on GitHub, you can:
1. Deploy to Render.com using `deploy_to_render.bat`
2. Or follow the instructions in `DEPLOYMENT_GUIDE.md`

## Troubleshooting

**Authentication Issues:**
- If you get authentication errors, you may need to:
  - Use a Personal Access Token instead of password
  - Or use GitHub Desktop for easier authentication
  - Or use SSH keys

**Repository Already Exists:**
- If you already created a repository on GitHub, just add it as remote and push
- If the repository has commits, use Option B above
