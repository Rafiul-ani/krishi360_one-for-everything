# 🌐 Deploy Krishi360 to Render - Get Live Link

## 🚀 **Quick Deploy to Render (5 minutes)**

### **Step 1: Create GitHub Repository**
1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it `krishi360` or any name you prefer
3. Upload all your project files to this repository

### **Step 2: Deploy to Render**
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Use these settings:

```
Name: krishi360
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

### **Step 3: Environment Variables (Optional)**
Add these in Render dashboard:
- `FLASK_ENV` = `production`
- `SECRET_KEY` = `your-secret-key-here`

### **Step 4: Deploy**
Click **"Create Web Service"** and wait 2-3 minutes for deployment.

## 🎉 **Your Live URL**
After deployment, you'll get a URL like:
**`https://krishi360.onrender.com`**

## 📋 **What's Included in Your Live App:**
- ✅ **4 User Roles:** Farmer, Buyer, Consultant, Admin
- ✅ **Bangladesh Currency:** ৳ (Taka)
- ✅ **Bangladesh Locations:** Dhaka, Rajshahi, Sylhet, Chittagong
- ✅ **Mobile Payments:** bKash, Nagad, Rocket
- ✅ **Complete Features:** Registration, Dashboards, Orders, Consultations

## 🔧 **Files Ready for Render:**
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Configured for production
- ✅ `render.yaml` - Render configuration
- ✅ All templates and static files

## 📱 **Test Your Live App:**
1. Visit your Render URL
2. Register as different user types
3. Test all features:
   - Farmer: Add crops, manage orders
   - Buyer: Browse crops, place orders
   - Consultant: Handle consultations
   - Admin: Manage platform

## 🆓 **Render Free Tier:**
- 750 hours/month free
- Automatic deployments from GitHub
- Custom domain support
- SSL certificate included

## 🚨 **Important Notes:**
- First deployment may take 3-5 minutes
- App sleeps after 15 minutes of inactivity (free tier)
- Wake up takes 30 seconds
- Database resets on each deployment (free tier)

## 🔄 **Update Your App:**
Just push changes to GitHub - Render auto-deploys!

---
**Your live Krishi360 platform will be accessible worldwide! 🌍**
