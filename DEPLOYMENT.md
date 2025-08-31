# 🚀 Krishi360 Deployment Guide

## Quick Deploy to Railway (Recommended)

### Step 1: Prepare Your Code
Your code is already prepared with:
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ Updated `app.py` - Configured for production

### Step 2: Deploy to Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and Deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Get Your Live URL:**
   Railway will provide you with a live URL like: `https://your-app-name.railway.app`

### Step 3: Set Environment Variables (if needed)
```bash
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=your-secret-key
```

## Alternative: Deploy to Render

1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3

## Alternative: Deploy to PythonAnywhere

1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create a free account
3. Upload your code via Git or file upload
4. Configure web app with Python 3.10
5. Set up virtual environment and install requirements

## Your Current Local URL
- **Local:** http://localhost:5000
- **Network:** http://127.0.0.1:5000

## After Deployment
Your live URL will be something like:
- Railway: `https://krishi360-production.railway.app`
- Render: `https://krishi360.onrender.com`
- PythonAnywhere: `https://yourusername.pythonanywhere.com`

## Features Available in Live Version
- ✅ User Registration/Login
- ✅ Farmer Dashboard
- ✅ Buyer Dashboard  
- ✅ Consultant Dashboard
- ✅ Crop Management
- ✅ Order System
- ✅ Consultation System
- ✅ Bangladesh Currency (৳)
- ✅ Bangladesh Locations
- ✅ Mobile Payment Methods (bKash, Nagad, Rocket)
