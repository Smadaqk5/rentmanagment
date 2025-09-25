#!/usr/bin/env python
"""
Heroku Deployment Script for Rental Management System
This script will help you deploy your Django app to Heroku
"""

import os
import subprocess
import sys
from pathlib import Path


def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    try:
        result = subprocess.run(['heroku', '--version'], capture_output=True, text=True, check=True)
        print(f"✅ Heroku CLI found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Heroku CLI not found!")
        print("\n📥 Please install Heroku CLI:")
        print("1. Go to: https://devcenter.heroku.com/articles/heroku-cli")
        print("2. Download and install for Windows")
        print("3. Restart your terminal")
        print("4. Run this script again")
        return False


def check_git():
    """Check if git is available"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
        print(f"✅ Git found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git not found. Please install Git first.")
        return False


def login_to_heroku():
    """Login to Heroku"""
    print("\n🔐 Please login to Heroku:")
    print("This will open a browser window for authentication...")
    
    try:
        result = subprocess.run(['heroku', 'login'], check=True)
        print("✅ Successfully logged in to Heroku!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to login to Heroku")
        return False


def create_heroku_app():
    """Create a new Heroku app"""
    print("\n🏗️ Creating Heroku app...")
    
    # Get app name from user
    app_name = input("Enter your Heroku app name (must be unique): ").strip()
    if not app_name:
        print("❌ App name is required!")
        return None
    
    try:
        # Create Heroku app
        result = subprocess.run(['heroku', 'create', app_name], capture_output=True, text=True, check=True)
        print(f"✅ Heroku app created: {app_name}")
        print(f"🌐 App URL: https://{app_name}.herokuapp.com")
        return app_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create Heroku app: {e.stderr}")
        return None


def set_environment_variables(app_name):
    """Set environment variables for Heroku"""
    print("\n🔧 Setting up environment variables...")
    
    # Your Africa's Talking credentials
    africas_talking_username = "smadaqk5"
    africas_talking_api_key = "atsk_0d6f9d0aabc3a50368896f809414ec0ad6909bf7c1dadeb65cf964e2423995cca9c2db28"
    
    # Generate a secret key
    import secrets
    secret_key = secrets.token_urlsafe(50)
    
    # Environment variables to set
    env_vars = {
        'SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'ALLOWED_HOSTS': f'{app_name}.herokuapp.com',
        'AFRICASTALKING_USERNAME': africas_talking_username,
        'AFRICASTALKING_API_KEY': africas_talking_api_key,
        'AFRICASTALKING_SENDER_ID': 'RENTAL'
    }
    
    print("Setting the following environment variables:")
    for key, value in env_vars.items():
        if key == 'AFRICASTALKING_API_KEY':
            display_value = f"{value[:20]}...{value[-10:]}"
        else:
            display_value = value
        print(f"  {key}: {display_value}")
    
    # Set each environment variable
    for key, value in env_vars.items():
        try:
            command = ['heroku', 'config:set', f'{key}={value}', '--app', app_name]
            subprocess.run(command, check=True, capture_output=True)
            print(f"✅ Set {key}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to set {key}: {e}")
            return False
    
    print("✅ All environment variables set successfully!")
    return True


def deploy_to_heroku(app_name):
    """Deploy the application to Heroku"""
    print(f"\n🚀 Deploying to Heroku app: {app_name}")
    
    try:
        # Add Heroku remote if not exists
        try:
            subprocess.run(['git', 'remote', 'add', 'heroku', f'https://git.heroku.com/{app_name}.git'], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Remote might already exist
            pass
        
        # Push to Heroku
        print("📤 Pushing code to Heroku...")
        result = subprocess.run(['git', 'push', 'heroku', 'main'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Code pushed to Heroku successfully!")
            return True
        else:
            print(f"❌ Failed to push to Heroku: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False


def run_heroku_commands(app_name):
    """Run post-deployment commands on Heroku"""
    print(f"\n🔧 Running post-deployment setup...")
    
    commands = [
        ['heroku', 'run', 'python', 'manage.py', 'migrate', '--app', app_name],
        ['heroku', 'run', 'python', 'manage.py', 'collectstatic', '--noinput', '--app', app_name]
    ]
    
    for command in commands:
        print(f"Running: {' '.join(command)}")
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("✅ Command completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {e.stderr}")
            return False
    
    return True


def create_superuser_instructions(app_name):
    """Provide instructions for creating superuser"""
    print(f"\n👤 Create Superuser Instructions:")
    print("=" * 50)
    print("To create a superuser for your app, run:")
    print(f"heroku run python manage.py createsuperuser --app {app_name}")
    print("\nThis will prompt you to enter:")
    print("- Username")
    print("- Email (optional)")
    print("- Password")
    print("\nAfter creating the superuser, you can login to your app!")


def main():
    """Main deployment function"""
    print("🚀 Heroku Deployment for Rental Management System")
    print("=" * 60)
    
    # Check prerequisites
    if not check_git():
        return
    
    if not check_heroku_cli():
        return
    
    # Login to Heroku
    if not login_to_heroku():
        return
    
    # Create Heroku app
    app_name = create_heroku_app()
    if not app_name:
        return
    
    # Set environment variables
    if not set_environment_variables(app_name):
        return
    
    # Deploy to Heroku
    if not deploy_to_heroku(app_name):
        return
    
    # Run post-deployment commands
    if not run_heroku_commands(app_name):
        return
    
    # Provide superuser instructions
    create_superuser_instructions(app_name)
    
    print(f"\n🎉 Deployment completed successfully!")
    print(f"🌐 Your app is available at: https://{app_name}.herokuapp.com")
    print("\n📋 Next steps:")
    print("1. Create a superuser (see instructions above)")
    print("2. Visit your app and login")
    print("3. Test the SMS functionality")
    print("4. Add your first tenant!")
    print("\n🎯 Your rental management system is now live on Heroku!")


if __name__ == "__main__":
    main()
