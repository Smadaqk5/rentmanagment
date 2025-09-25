# 🗄️ Heroku Database Setup Guide

## Database Options for Your Rental Management System

### Option 1: SQLite (Default - No Setup Required)
Your app is already configured to use SQLite when no database credentials are provided.

**Pros:**
- ✅ No setup required
- ✅ Free
- ✅ Perfect for testing

**Cons:**
- ❌ Data resets when app restarts
- ❌ Not suitable for production

**Setup:** No additional steps needed!

### Option 2: Heroku Postgres (Recommended for Production)

#### Step 1: Add Heroku Postgres
1. Go to your Heroku app dashboard
2. Click "Resources" tab
3. Search for "Heroku Postgres"
4. Click "Add-ons" → "Heroku Postgres"
5. Choose "Hobby Dev" (free tier)
6. Click "Provision"

#### Step 2: Verify Database
1. Go to "Settings" → "Config Vars"
2. You should see `DATABASE_URL` automatically added
3. Your app will automatically use PostgreSQL

#### Step 3: Run Migrations
1. Go to "More" → "Run console"
2. Run: `python manage.py migrate`

### Option 3: Supabase (Your Current Setup)

#### Step 1: Get Supabase Credentials
1. Go to your Supabase project dashboard
2. Go to Settings → Database
3. Copy your database credentials

#### Step 2: Set Environment Variables
In your Heroku app dashboard, go to "Settings" → "Config Vars" and add:

```
SUPABASE_URL = https://your-project.supabase.co
SUPABASE_KEY = your-supabase-anon-key
SUPABASE_DB_NAME = postgres
SUPABASE_DB_USER = postgres
SUPABASE_DB_PASSWORD = your-database-password
SUPABASE_DB_HOST = db.your-project.supabase.co
SUPABASE_DB_PORT = 5432
```

#### Step 3: Run Migrations
1. Go to "More" → "Run console"
2. Run: `python manage.py migrate`

## 🎯 Recommended Setup

### For Testing/Development:
**Use SQLite** - No additional setup needed!

### For Production:
**Use Heroku Postgres** - Free tier available, reliable, and scalable

## 📊 Database Features

Your rental management system includes:
- ✅ **Tenant Management** - Store tenant information
- ✅ **Payment Tracking** - Record all payments
- ✅ **SMS Logs** - Track SMS delivery status
- ✅ **Archive System** - Store deleted records
- ✅ **History Tracking** - Log all changes
- ✅ **Analytics** - Calculate statistics

## 🔧 Troubleshooting

### Common Issues:
1. **Database connection errors**
   - Check environment variables
   - Verify database credentials
   - Run migrations

2. **Migration errors**
   - Check database permissions
   - Verify table creation
   - Check logs for specific errors

### Useful Commands:
```bash
# Check database connection
python manage.py dbshell

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check database status
python manage.py showmigrations
```

## 🎉 Success!

Once your database is set up, you'll have:
- ✅ **Persistent data storage**
- ✅ **Full tenant management**
- ✅ **Payment tracking**
- ✅ **SMS integration**
- ✅ **Analytics and reporting**

---

**Choose the database option that best fits your needs! 🚀**
