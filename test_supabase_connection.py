#!/usr/bin/env python
"""
Test Supabase database connection
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
django.setup()

from django.db import connection
from django.conf import settings


def test_database_connection():
    """Test database connection"""
    print("🔍 Testing Supabase Database Connection")
    print("=" * 50)
    
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
        print("\n🔧 Troubleshooting steps:")
        print("1. Check your Supabase project is active")
        print("2. Verify your database credentials")
        print("3. Check network restrictions in Supabase")
        print("4. Ensure your IP is whitelisted")
        
        return False


def check_environment_variables():
    """Check if Supabase environment variables are set"""
    print("\n🔍 Checking Environment Variables")
    print("=" * 40)
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY', 
        'SUPABASE_DB_NAME',
        'SUPABASE_DB_USER',
        'SUPABASE_DB_PASSWORD',
        'SUPABASE_DB_HOST',
        'SUPABASE_DB_PORT'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'SUPABASE_DB_PASSWORD':
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ All required environment variables are set!")
        return True


def main():
    """Main function"""
    print("🚀 Supabase Connection Troubleshooter")
    print("=" * 60)
    
    # Check environment variables
    env_ok = check_environment_variables()
    
    if not env_ok:
        print("\n❌ Please set all required environment variables first!")
        return
    
    # Test database connection
    connection_ok = test_database_connection()
    
    if connection_ok:
        print("\n🎉 Supabase connection is working!")
        print("✅ Your rental management system should work now!")
    else:
        print("\n🔧 Please fix the connection issues above")


if __name__ == "__main__":
    main()
