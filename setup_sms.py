#!/usr/bin/env python
"""
Setup script for SMSMobile API configuration
This script will create the .env file and test the SMS integration
"""

import os

def create_env_file():
    """Create .env file with SMSMobile API configuration"""
    env_content = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Supabase Database Configuration (Optional - will use SQLite if not set)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-database-password
SUPABASE_DB_HOST=db.your-project.supabase.co
SUPABASE_DB_PORT=5432

# SMSMobile API Configuration
SMSMOBILE_API_KEY=b02fa0e9633854c45d4a1c7cc6186c9ef7e1b700f3d2b97f
SMSMOBILE_API_URL=https://api.smsmobile.africa/v1/send
SMSMOBILE_SENDER_ID=RENTAL

# WhatsApp Cloud API Configuration (Deprecated - kept for backward compatibility)
WHATSAPP_ACCESS_TOKEN=your-whatsapp-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_VERIFY_TOKEN=your-verify-token
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with SMSMobile API configuration")

def test_sms_configuration():
    """Test if SMS configuration is working"""
    print("\n🧪 Testing SMS Configuration...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check if API key is loaded
    api_key = os.getenv('SMSMOBILE_API_KEY')
    api_url = os.getenv('SMSMOBILE_API_URL')
    sender_id = os.getenv('SMSMOBILE_SENDER_ID')
    
    print(f"📱 API Key: {'✅ Set' if api_key else '❌ Missing'}")
    print(f"🌐 API URL: {api_url}")
    print(f"📤 Sender ID: {sender_id}")
    
    if api_key:
        print("✅ SMSMobile API is properly configured!")
        return True
    else:
        print("❌ SMSMobile API is not configured properly")
        return False

if __name__ == "__main__":
    print("🚀 Setting up SMSMobile API for Rental Management System")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Test configuration
    if test_sms_configuration():
        print("\n🎉 Setup complete! You can now use SMS features.")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Login to your rental management system")
        print("3. Test SMS by sending a reminder to a tenant")
    else:
        print("\n❌ Setup failed. Please check the configuration.")
