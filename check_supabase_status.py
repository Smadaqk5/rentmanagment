#!/usr/bin/env python
"""
Check Supabase connection status and project health
"""

import os
import sys
import django
import requests
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
django.setup()

from django.db import connection
from django.conf import settings


def check_supabase_project_status():
    """Check if Supabase project is accessible"""
    print("🔍 Checking Supabase Project Status")
    print("=" * 50)
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase credentials not found in environment")
        return False
    
    try:
        # Test Supabase API endpoint
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        # Test the Supabase API
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Supabase API is accessible")
            print(f"✅ Project URL: {supabase_url}")
            return True
        else:
            print(f"❌ Supabase API returned status: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Supabase API")
        print("💡 Possible issues:")
        print("   - Project is paused or inactive")
        print("   - Network connectivity issues")
        print("   - Wrong Supabase URL")
        return False
    except requests.exceptions.Timeout:
        print("❌ Supabase API request timed out")
        print("💡 Project might be paused or slow to respond")
        return False
    except Exception as e:
        print(f"❌ Error checking Supabase: {e}")
        return False


def check_database_connection():
    """Check database connection"""
    print("\n🔍 Checking Database Connection")
    print("=" * 40)
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        print("✅ Database connection successful!")
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Database name: {settings.DATABASES['default']['NAME']}")
        print(f"✅ Database host: {settings.DATABASES['default']['HOST']}")
        print(f"✅ Database port: {settings.DATABASES['default']['PORT']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_environment_variables():
    """Check Supabase environment variables"""
    print("\n🔍 Checking Environment Variables")
    print("=" * 40)
    
    required_vars = {
        'SUPABASE_URL': 'Supabase project URL',
        'SUPABASE_KEY': 'Supabase anon key',
        'SUPABASE_DB_NAME': 'Database name',
        'SUPABASE_DB_USER': 'Database user',
        'SUPABASE_DB_PASSWORD': 'Database password',
        'SUPABASE_DB_HOST': 'Database host',
        'SUPABASE_DB_PORT': 'Database port'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            if var == 'SUPABASE_DB_PASSWORD':
                print(f"✅ {var}: {'*' * len(value)} ({description})")
            else:
                print(f"✅ {var}: {value} ({description})")
        else:
            print(f"❌ {var}: Not set ({description})")
            missing_vars.append(var)
    
    return len(missing_vars) == 0


def check_heroku_environment():
    """Check if running on Heroku"""
    print("\n🔍 Checking Deployment Environment")
    print("=" * 40)
    
    if os.getenv('DYNO'):
        print("✅ Running on Heroku")
        print(f"✅ Dyno: {os.getenv('DYNO')}")
        return True
    else:
        print("ℹ️  Running locally")
        return False


def main():
    """Main function"""
    print("🚀 Supabase Connection Status Checker")
    print("=" * 60)
    
    # Check environment
    env_ok = check_environment_variables()
    heroku_env = check_heroku_environment()
    
    if not env_ok:
        print("\n❌ Missing environment variables!")
        print("💡 Please set all required Supabase environment variables")
        return
    
    # Check Supabase project status
    supabase_ok = check_supabase_project_status()
    
    # Check database connection
    db_ok = check_database_connection()
    
    # Summary
    print("\n📊 Connection Status Summary")
    print("=" * 40)
    print(f"Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"Supabase API: {'✅' if supabase_ok else '❌'}")
    print(f"Database Connection: {'✅' if db_ok else '❌'}")
    
    if env_ok and supabase_ok and db_ok:
        print("\n🎉 Supabase is fully connected and working!")
        print("✅ Your rental management system should work perfectly!")
    else:
        print("\n🔧 Issues found:")
        if not env_ok:
            print("   - Missing environment variables")
        if not supabase_ok:
            print("   - Supabase project is not accessible")
            print("   - Check if project is paused or inactive")
        if not db_ok:
            print("   - Database connection failed")
            print("   - Check database credentials and network settings")
        
        print("\n💡 Recommended fixes:")
        print("1. Check your Supabase project status")
        print("2. Verify all environment variables are correct")
        print("3. Check network restrictions in Supabase")
        print("4. Consider switching to Heroku Postgres for easier deployment")


if __name__ == "__main__":
    main()
