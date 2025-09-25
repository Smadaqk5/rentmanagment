# 🚀 Heroku Deployment Guide

## Step-by-Step Heroku Deployment for Rental Management System

### Prerequisites
- GitHub repository: https://github.com/Smadaqk5/rentmanagment.git
- Heroku account (free)
- Git installed

### Step 1: Install Heroku CLI

1. **Download Heroku CLI**
   - Go to: https://devcenter.heroku.com/articles/heroku-cli
   - Download for Windows
   - Install the downloaded file

2. **Verify Installation**
   ```bash
   heroku --version
   ```

### Step 2: Login to Heroku

```bash
heroku login
```
*This will open a browser window for authentication*

### Step 3: Create Heroku App

```bash
heroku create your-rental-app-name
```
*Replace `your-rental-app-name` with a unique name*

### Step 4: Set Environment Variables

```bash
# Set Django settings
heroku config:set SECRET_KEY="your-super-secret-key-here" --app your-app-name
heroku config:set DEBUG=False --app your-app-name
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com" --app your-app-name

# Set Africa's Talking SMS credentials
heroku config:set AFRICASTALKING_USERNAME="smadaqk5" --app your-app-name
heroku config:set AFRICASTALKING_API_KEY="atsk_0d6f9d0aabc3a50368896f809414ec0ad6909bf7c1dadeb65cf964e2423995cca9c2db28" --app your-app-name
heroku config:set AFRICASTALKING_SENDER_ID="RENTAL" --app your-app-name
```

### Step 5: Deploy to Heroku

```bash
# Add Heroku remote
git remote add heroku https://git.heroku.com/your-app-name.git

# Deploy
git push heroku main
```

### Step 6: Run Database Migrations

```bash
heroku run python manage.py migrate --app your-app-name
```

### Step 7: Collect Static Files

```bash
heroku run python manage.py collectstatic --noinput --app your-app-name
```

### Step 8: Create Superuser

```bash
heroku run python manage.py createsuperuser --app your-app-name
```

### Step 9: Open Your App

```bash
heroku open --app your-app-name
```

## 🎉 Success!

Your rental management system is now live at:
**https://your-app-name.herokuapp.com**

## 📱 Test Your SMS Integration

1. **Login** to your app
2. **Add a tenant** with a real phone number
3. **Send SMS reminder** to test Africa's Talking
4. **Check SMS logs** for delivery status

## 🔧 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` has all dependencies
   - Ensure `Procfile` exists
   - Check Heroku logs: `heroku logs --tail --app your-app-name`

2. **Database Errors**
   - Run migrations: `heroku run python manage.py migrate --app your-app-name`
   - Check database connection

3. **SMS Not Working**
   - Verify environment variables are set
   - Check Africa's Talking account credits
   - Test with real phone number

4. **Static Files Not Loading**
   - Run: `heroku run python manage.py collectstatic --noinput --app your-app-name`
   - Check `STATIC_ROOT` in settings

### Useful Commands:

```bash
# Check app status
heroku ps --app your-app-name

# View logs
heroku logs --tail --app your-app-name

# Run Django shell
heroku run python manage.py shell --app your-app-name

# Check environment variables
heroku config --app your-app-name

# Restart app
heroku restart --app your-app-name
```

## 🎯 Your App Features

Once deployed, you'll have:
- ✅ **Full rental management system**
- ✅ **SMS notifications via Africa's Talking**
- ✅ **Analytics and reporting**
- ✅ **Archive/history system**
- ✅ **Responsive web interface**

## 📞 Support

If you encounter issues:
1. Check Heroku logs: `heroku logs --tail --app your-app-name`
2. Verify environment variables: `heroku config --app your-app-name`
3. Test SMS functionality with real phone numbers
4. Ensure Africa's Talking account has credits

---

**Your rental management system is now live on Heroku! 🚀🏠**
