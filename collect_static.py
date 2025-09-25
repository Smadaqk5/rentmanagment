#!/usr/bin/env python
"""
Collect static files for production deployment
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def collect_static_files():
    """Collect static files for production"""
    print("🔄 Collecting static files for production...")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
    django.setup()
    
    # Collect static files
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected successfully!")
        print("📁 Static files are now in the 'staticfiles' directory")
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")

if __name__ == "__main__":
    collect_static_files()


