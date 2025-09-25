# 🚀 Rental Management System - Deployment Guide

## ⚠️ Important Note About Netlify

**Netlify is for static sites only** (HTML, CSS, JavaScript). Your Django application is a dynamic web application that requires a Python server. 

**Recommended platforms for Django deployment:**
- **Heroku** (easiest for beginners)
- **Railway** (modern alternative to Heroku)
- **Render** (free tier available)
- **DigitalOcean App Platform**

## 🎯 Quick Deployment Options

### Option 1: Heroku (Recommended for Beginners)

1. **Create Heroku Account**
   - Go to [heroku.com](https://heroku.com)
   - Sign up for a free account

2. **Install Heroku CLI**
   - Download from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

3. **Deploy to Heroku**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create a new Heroku app
   heroku create your-rental-app-name
   
   # Set environment variables
   heroku config:set SECRET_KEY="your-super-secret-key-here"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
   
   # Set database (use Supabase)
   heroku config:set SUPABASE_URL="https://your-project.supabase.co"
   heroku config:set SUPABASE_KEY="your-supabase-anon-key"
   heroku config:set SUPABASE_DB_NAME="postgres"
   heroku config:set SUPABASE_DB_USER="postgres"
   heroku config:set SUPABASE_DB_PASSWORD="your-database-password"
   heroku config:set SUPABASE_DB_HOST="db.your-project.supabase.co"
   heroku config:set SUPABASE_DB_PORT="5432"
   
   # Set SMS API
   heroku config:set SMSMOBILE_API_KEY="b02fa0e9633854c45d4a1c7cc6186c9ef7e1b700f3d2b97f"
   heroku config:set SMSMOBILE_API_URL="https://api.smsmobileapi.com/sendsms"
   heroku config:set SMSMOBILE_SENDER_ID="RENTAL"
   
   # Deploy
   git add .
   git commit -m "Deploy rental management system"
   git push heroku main
   
   # Run migrations
   heroku run python manage.py migrate
   
   # Create superuser
   heroku run python manage.py createsuperuser
   ```

### Option 2: Railway (Modern Alternative)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Connect your GitHub repository
   - Railway will automatically detect Django
   - Set environment variables in Railway dashboard
   - Deploy automatically

### Option 3: Render (Free Tier Available)

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for free

2. **Create Web Service**
   - Connect your GitHub repository
   - Choose "Web Service"
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn rental_management.wsgi:application`
   - Set environment variables

## 📋 Pre-Deployment Checklist

### ✅ Files Already Created for You:
- `Procfile` - Tells the platform how to run your app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Updated with production dependencies
- `rental_management/settings.py` - Updated for production

### 🔧 Environment Variables to Set:

```bash
# Required for all platforms
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-domain.com

# Database (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-database-password
SUPABASE_DB_HOST=db.your-project.supabase.co
SUPABASE_DB_PORT=5432

# Africa's Talking SMS API
AFRICASTALKING_USERNAME=your_username
AFRICASTALKING_API_KEY=your_africas_talking_api_key
AFRICASTALKING_SENDER_ID=RENTAL

# SMSMobile API (Legacy)
SMSMOBILE_API_KEY=b02fa0e9633854c45d4a1c7cc6186c9ef7e1b700f3d2b97f
SMSMOBILE_API_URL=https://api.smsmobileapi.com/sendsms
SMSMOBILE_SENDER_ID=RENTAL
```

## 🗄️ Database Setup (Supabase)

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Get your database credentials

2. **Update Environment Variables**
   - Use the Supabase credentials in your deployment platform

## 📱 SMS Configuration (Africa's Talking)

Your rental management system now uses **Africa's Talking** for SMS functionality:

### Getting Africa's Talking Credentials:

1. **Create Account**
   - Go to [africastalking.com](https://africastalking.com)
   - Sign up for a free account

2. **Get API Credentials**
   - Login to your dashboard
   - Go to Settings → API Keys
   - Generate a new API key
   - Note your username (usually your account name)

3. **Request Sender ID**
   - Go to SMS → Alphanumerics
   - Request a sender ID (e.g., "RENTAL")
   - Wait for approval (usually instant for alphanumeric)

4. **Configure Environment Variables**
   ```bash
   AFRICASTALKING_USERNAME=your_username
   AFRICASTALKING_API_KEY=your_api_key
   AFRICASTALKING_SENDER_ID=RENTAL
   ```

### Testing SMS:
- Use `sandbox` as username for testing
- Test with dummy numbers first
- Verify SMS delivery in Africa's Talking dashboard

## 🚀 Post-Deployment Steps

1. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

2. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Test Your Application**
   - Visit your deployed URL
   - Login with your superuser credentials
   - Test SMS functionality

## 🔒 Security Notes

- **Never commit `.env` files** to version control
- **Use strong SECRET_KEY** in production
- **Set DEBUG=False** in production
- **Use HTTPS** in production
- **Keep API keys secure**

## 📞 Support

If you encounter issues:
1. Check the platform's logs
2. Verify environment variables are set correctly
3. Ensure database is accessible
4. Test SMS API connectivity

## 🎉 Success!

Once deployed, you'll have:
- ✅ Full rental management system
- ✅ SMS notifications via SMSMobile API
- ✅ Tenant and payment tracking
- ✅ Analytics and reporting
- ✅ Archive/history system
- ✅ Responsive web interface

Your rental management system will be accessible at your deployed URL!


