#!/usr/bin/env python
"""
Setup script for Rental Management System
Run this script to initialize the project
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return False

def main():
    print("🏠 Rental Management System Setup")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("Please copy env.example to .env and configure your settings:")
        print("cp env.example .env")
        print("\nThen edit .env with your Supabase and WhatsApp credentials.")
        return
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
    django.setup()
    
    # Run Django commands
    commands = [
        ("python manage.py makemigrations", "Creating database migrations"),
        ("python manage.py migrate", "Applying database migrations"),
        ("python manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Setup failed at: {description}")
            return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Create a landlord user: python manage.py setup_landlord")
    print("2. Start the development server: python manage.py runserver")
    print("3. Open http://127.0.0.1:8000 in your browser")
    print("\nFor detailed setup instructions, see README.md")

if __name__ == "__main__":
    main()
