#!/usr/bin/env python
"""
Manual Heroku Deployment Guide for Rental Management System
This script provides step-by-step instructions for manual deployment
"""

import os
import subprocess
import sys


def print_step(step_num, title, commands, description=""):
    """Print a deployment step"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")
    if description:
        print(f"📝 {description}")
    print(f"\n🔧 Commands to run:")
    for i, cmd in enumerate(commands, 1):
        print(f"   {i}. {cmd}")
    print(f"\n⏳ After running these commands, press Enter to continue...")


def main():
    """Main deployment guide"""
    print("🚀 Manual Heroku Deployment for Rental Management System")
    print("=" * 70)
    
    print("\n📋 PREREQUISITES CHECK:")
    print("✅ GitHub repository: https://github.com/Smadaqk5/rentmanagment.git")
    print("✅ Heroku CLI: Should be installed")
    print("✅ Git: Available")
    print("✅ Python: Available")
    
    # Step 1: Login to Heroku
    print_step(
        1, 
        "Login to Heroku",
        ["heroku login"],
        "This will open a browser window for authentication"
    )
    input()
    
    # Step 2: Create Heroku app
    print_step(
        2,
        "Create Heroku App",
        ["heroku create your-rental-app-name"],
        "Replace 'your-rental-app-name' with a unique name (e.g., 'my-rental-system-2024')"
    )
    input()
    
    # Step 3: Set environment variables
    print_step(
        3,
        "Set Environment Variables",
        [
            'heroku config:set SECRET_KEY="your-super-secret-key-here" --app your-app-name',
            'heroku config:set DEBUG=False --app your-app-name',
            'heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com" --app your-app-name',
            'heroku config:set AFRICASTALKING_USERNAME="smadaqk5" --app your-app-name',
            'heroku config:set AFRICASTALKING_API_KEY="atsk_0d6f9d0aabc3a50368896f809414ec0ad6909bf7c1dadeb65cf964e2423995cca9c2db28" --app your-app-name',
            'heroku config:set AFRICASTALKING_SENDER_ID="RENTAL" --app your-app-name'
        ],
        "Set all required environment variables for your app"
    )
    input()
    
    # Step 4: Deploy to Heroku
    print_step(
        4,
        "Deploy to Heroku",
        [
            "git add .",
            "git commit -m 'Deploy to Heroku'",
            "git push heroku main"
        ],
        "Deploy your code to Heroku"
    )
    input()
    
    # Step 5: Run migrations
    print_step(
        5,
        "Run Database Migrations",
        ["heroku run python manage.py migrate --app your-app-name"],
        "Set up the database on Heroku"
    )
    input()
    
    # Step 6: Collect static files
    print_step(
        6,
        "Collect Static Files",
        ["heroku run python manage.py collectstatic --noinput --app your-app-name"],
        "Prepare static files for production"
    )
    input()
    
    # Step 7: Create superuser
    print_step(
        7,
        "Create Superuser",
        ["heroku run python manage.py createsuperuser --app your-app-name"],
        "Create an admin user for your app"
    )
    input()
    
    # Step 8: Open app
    print_step(
        8,
        "Open Your App",
        ["heroku open --app your-app-name"],
        "Open your deployed app in the browser"
    )
    input()
    
    print("\n🎉 DEPLOYMENT COMPLETED!")
    print("=" * 50)
    print("✅ Your rental management system is now live!")
    print("🌐 App URL: https://your-app-name.herokuapp.com")
    print("\n📱 Features available:")
    print("  • Tenant management")
    print("  • Payment tracking")
    print("  • SMS notifications via Africa's Talking")
    print("  • Analytics and reporting")
    print("  • Archive/history system")
    
    print("\n🔧 Troubleshooting:")
    print("  • Check logs: heroku logs --tail --app your-app-name")
    print("  • Restart app: heroku restart --app your-app-name")
    print("  • Check config: heroku config --app your-app-name")


if __name__ == "__main__":
    main()
