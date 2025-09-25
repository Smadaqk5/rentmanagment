#!/usr/bin/env python
"""
Check rental management app status and accessibility
"""

import requests
import os
from pathlib import Path


def check_heroku_app_status():
    """Check if Heroku app is accessible"""
    print("🔍 Checking Heroku App Status")
    print("=" * 40)
    
    # Your Heroku app URL
    app_url = "https://rent-7d65f297e545.herokuapp.com"
    
    try:
        print(f"🌐 Testing app URL: {app_url}")
        response = requests.get(app_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ App is accessible!")
            print("✅ App is responding to requests")
            return True
        elif response.status_code == 500:
            print("❌ App has internal server error")
            print("💡 This is likely the database connection issue")
            return False
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to app")
        print("💡 App might be down or not deployed")
        return False
    except requests.exceptions.Timeout:
        print("❌ App request timed out")
        print("💡 App might be slow to respond")
        return False
    except Exception as e:
        print(f"❌ Error checking app: {e}")
        return False


def check_database_connection():
    """Check if database connection is working"""
    print("\n🔍 Checking Database Connection")
    print("=" * 40)
    
    try:
        # Test database connection
        import django
        from django.conf import settings
        
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Checking Environment Variables")
    print("=" * 40)
    
    required_vars = [
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'AFRICASTALKING_USERNAME',
        'AFRICASTALKING_API_KEY',
        'AFRICASTALKING_SENDER_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'SECRET_KEY':
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    return len(missing_vars) == 0


def main():
    """Main function"""
    print("🚀 Rental Management App Status Checker")
    print("=" * 60)
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    # Check database connection
    db_ok = check_database_connection()
    
    # Check app status
    app_ok = check_heroku_app_status()
    
    # Summary
    print("\n📊 App Status Summary")
    print("=" * 40)
    print(f"Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"Database Connection: {'✅' if db_ok else '❌'}")
    print(f"App Accessibility: {'✅' if app_ok else '❌'}")
    
    if env_ok and db_ok and app_ok:
        print("\n🎉 Your app is fully working!")
        print("✅ You can login at: https://rent-7d65f297e545.herokuapp.com")
        print("✅ Use your superuser credentials to login")
    else:
        print("\n🔧 Issues found:")
        if not env_ok:
            print("   - Missing environment variables")
        if not db_ok:
            print("   - Database connection failed")
        if not app_ok:
            print("   - App is not accessible")
        
        print("\n💡 Next steps:")
        print("1. Fix database connection (add Heroku Postgres or fix Supabase)")
        print("2. Check environment variables in Heroku")
        print("3. Restart your Heroku app")
        print("4. Test your app URL")


if __name__ == "__main__":
    main()
