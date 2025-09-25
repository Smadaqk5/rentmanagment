#!/usr/bin/env python
"""
Heroku Deployment Script for Rental Management System
This script helps you deploy your Django app to Heroku
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_heroku_cli():
    """Check if Heroku CLI is installed"""
    result = run_command("heroku --version", "Checking Heroku CLI")
    if result:
        print(f"✅ Heroku CLI found: {result.strip()}")
        return True
    else:
        print("❌ Heroku CLI not found. Please install it from: https://devcenter.heroku.com/articles/heroku-cli")
        return False

def check_git():
    """Check if git is available"""
    result = run_command("git --version", "Checking Git")
    if result:
        print(f"✅ Git found: {result.strip()}")
        return True
    else:
        print("❌ Git not found. Please install Git first.")
        return False

def create_heroku_app(app_name):
    """Create a new Heroku app"""
    if not app_name:
        app_name = input("Enter your Heroku app name (must be unique): ")
    
    command = f"heroku create {app_name}"
    result = run_command(command, f"Creating Heroku app '{app_name}'")
    return result is not None

def set_environment_variables():
    """Set environment variables for Heroku"""
    print("\n🔧 Setting up environment variables...")
    
    # Get user input for configuration
    secret_key = input("Enter a secret key for Django (or press Enter for auto-generated): ")
    if not secret_key:
        secret_key = "django-insecure-" + os.urandom(32).hex()
    
    app_name = input("Enter your Heroku app name: ")
    
    # Database configuration
    print("\n📊 Database Configuration (Supabase):")
    supabase_url = input("Enter Supabase URL: ")
    supabase_key = input("Enter Supabase anon key: ")
    supabase_db_name = input("Enter database name (default: postgres): ") or "postgres"
    supabase_db_user = input("Enter database user (default: postgres): ") or "postgres"
    supabase_db_password = input("Enter database password: ")
    supabase_db_host = input("Enter database host: ")
    supabase_db_port = input("Enter database port (default: 5432): ") or "5432"
    
    # Set environment variables
    env_vars = {
        'SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'ALLOWED_HOSTS': f'{app_name}.herokuapp.com',
        'SUPABASE_URL': supabase_url,
        'SUPABASE_KEY': supabase_key,
        'SUPABASE_DB_NAME': supabase_db_name,
        'SUPABASE_DB_USER': supabase_db_user,
        'SUPABASE_DB_PASSWORD': supabase_db_password,
        'SUPABASE_DB_HOST': supabase_db_host,
        'SUPABASE_DB_PORT': supabase_db_port,
        'SMSMOBILE_API_KEY': 'b02fa0e9633854c45d4a1c7cc6186c9ef7e1b700f3d2b97f',
        'SMSMOBILE_API_URL': 'https://api.smsmobileapi.com/sendsms',
        'SMSMOBILE_SENDER_ID': 'RENTAL'
    }
    
    for key, value in env_vars.items():
        command = f'heroku config:set {key}="{value}"'
        run_command(command, f"Setting {key}")
    
    return True

def deploy_to_heroku():
    """Deploy the application to Heroku"""
    print("\n🚀 Deploying to Heroku...")
    
    # Add and commit changes
    run_command("git add .", "Adding files to git")
    run_command('git commit -m "Deploy rental management system"', "Committing changes")
    
    # Push to Heroku
    result = run_command("git push heroku main", "Pushing to Heroku")
    return result is not None

def run_post_deployment():
    """Run post-deployment tasks"""
    print("\n🔧 Running post-deployment tasks...")
    
    # Run migrations
    run_command("heroku run python manage.py migrate", "Running database migrations")
    
    # Collect static files
    run_command("heroku run python manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n✅ Post-deployment tasks completed!")
    print("🎉 Your app should now be deployed!")
    print("📝 Don't forget to create a superuser:")
    print("   heroku run python manage.py createsuperuser")

def main():
    """Main deployment function"""
    print("🚀 Heroku Deployment Script for Rental Management System")
    print("=" * 60)
    
    # Check prerequisites
    if not check_heroku_cli():
        return
    
    if not check_git():
        return
    
    # Login to Heroku
    print("\n🔐 Please login to Heroku:")
    run_command("heroku login", "Logging into Heroku")
    
    # Get app name
    app_name = input("\nEnter your Heroku app name (must be unique): ")
    
    # Create app
    if not create_heroku_app(app_name):
        print("❌ Failed to create Heroku app")
        return
    
    # Set environment variables
    if not set_environment_variables():
        print("❌ Failed to set environment variables")
        return
    
    # Deploy
    if not deploy_to_heroku():
        print("❌ Failed to deploy to Heroku")
        return
    
    # Post-deployment tasks
    run_post_deployment()
    
    print(f"\n🎉 Deployment completed!")
    print(f"🌐 Your app is available at: https://{app_name}.herokuapp.com")
    print("\n📋 Next steps:")
    print("1. Create a superuser: heroku run python manage.py createsuperuser")
    print("2. Visit your app and login")
    print("3. Test the SMS functionality")
    print("4. Add your first tenant!")

if __name__ == "__main__":
    main()


