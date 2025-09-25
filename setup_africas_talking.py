#!/usr/bin/env python
"""
Setup Africa's Talking SMS configuration for Rental Management System
"""

import os
from pathlib import Path


def setup_africas_talking():
    """Setup Africa's Talking configuration with user's credentials"""
    print("🔧 Setting up Africa's Talking SMS configuration...")
    print("=" * 60)
    
    # User's credentials
    username = "smadaqk5"
    api_key = "atsk_0d6f9d0aabc3a50368896f809414ec0ad6909bf7c1dadeb65cf964e2423995cca9c2db28"
    sender_id = "RENTAL"
    
    print(f"✅ Username: {username}")
    print(f"✅ API Key: {api_key[:20]}...{api_key[-10:]}")
    print(f"✅ Sender ID: {sender_id}")
    
    # Create .env file content
    env_content = f"""# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True

# Africa's Talking SMS Configuration
AFRICASTALKING_USERNAME={username}
AFRICASTALKING_API_KEY={api_key}
AFRICASTALKING_SENDER_ID={sender_id}

# SMSMobile API Configuration (Legacy)
SMSMOBILE_API_KEY=b02fa0e9633854c45d4a1c7cc6186c9ef7e1b700f3d2b97f
SMSMOBILE_API_URL=https://api.smsmobileapi.com/sendsms
SMSMOBILE_SENDER_ID=RENTAL

# WhatsApp Cloud API Configuration (Deprecated - kept for backward compatibility)
WHATSAPP_ACCESS_TOKEN=your-whatsapp-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_VERIFY_TOKEN=your-verify-token
"""
    
    # Write .env file
    env_file = Path(".env")
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ .env file created successfully!")
        print(f"📁 Location: {env_file.absolute()}")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    # Test the configuration
    print("\n🧪 Testing Africa's Talking configuration...")
    return test_africas_talking_config()


def test_africas_talking_config():
    """Test the Africa's Talking configuration"""
    try:
        # Import Django settings
        import django
        from django.conf import settings
        
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
        django.setup()
        
        # Test the service
        from rental_app.africas_talking_service import AfricasTalkingService
        
        sms_service = AfricasTalkingService()
        
        # Test connection
        print("1. Testing connection...")
        success, message = sms_service.test_connection()
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
            return False
        
        # Test phone number formatting
        print("\n2. Testing phone number formatting...")
        test_numbers = [
            "0712345678",
            "254712345678", 
            "+254712345678"
        ]
        
        for number in test_numbers:
            formatted = sms_service._format_phone_number(number)
            print(f"   {number} → {formatted}")
        
        # Test SMS sending (with dummy data - won't actually send)
        print("\n3. Testing SMS service initialization...")
        test_phone = "+254700000000"  # Dummy number
        test_message = "Test message from Rental Management System"
        
        print(f"   Service initialized: ✅")
        print(f"   Username: {sms_service.username}")
        print(f"   Sender ID: {sms_service.sender_id}")
        print(f"   API Key configured: {'✅' if sms_service.api_key else '❌'}")
        
        print("\n🎉 Africa's Talking configuration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Africa's Talking SMS Setup for Rental Management System")
    print("=" * 70)
    
    # Setup configuration
    if setup_africas_talking():
        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run your Django server: python manage.py runserver")
        print("2. Test SMS functionality in your web interface")
        print("3. Deploy your application with the new SMS service")
        print("\n🎯 Your SMS service is now ready with Africa's Talking!")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
