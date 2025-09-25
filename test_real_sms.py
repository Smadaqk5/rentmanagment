#!/usr/bin/env python
"""
Test SMS with real phone number
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

from rental_app.africas_talking_service import AfricasTalkingService


def test_real_sms():
    """Test SMS with real phone number"""
    print("📱 Testing SMS with Real Phone Number")
    print("=" * 50)
    
    # Get phone number from user
    phone_number = input("Enter a real phone number to test SMS (e.g., 0712345678): ").strip()
    if not phone_number:
        print("❌ Phone number is required!")
        return False
    
    # Initialize SMS service
    sms_service = AfricasTalkingService()
    
    # Test message
    test_message = "Hello! This is a test message from your Rental Management System. SMS is working perfectly! 🎉"
    
    print(f"\n📤 Sending SMS to: {phone_number}")
    print(f"📝 Message: {test_message}")
    print(f"👤 Sender ID: {sms_service.sender_id}")
    
    # Send SMS
    success, message = sms_service.send_sms(phone_number, test_message)
    
    if success:
        print(f"\n✅ {message}")
        print("🎉 SMS sent successfully! Check your phone!")
        return True
    else:
        print(f"\n❌ {message}")
        print("💡 This might be because:")
        print("   - The phone number format is incorrect")
        print("   - Your Africa's Talking account needs verification")
        print("   - You're using sandbox mode (use 'sandbox' as username for testing)")
        print("   - Your account doesn't have credits")
        return False


def main():
    """Main function"""
    print("🚀 Real SMS Test for Rental Management System")
    print("=" * 60)
    
    print("⚠️  Note: This will send a real SMS to the phone number you provide.")
    print("   Make sure you have sufficient credits in your Africa's Talking account.")
    
    confirm = input("\nDo you want to proceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Test cancelled.")
        return
    
    if test_real_sms():
        print("\n🎯 SMS functionality is working perfectly!")
        print("✅ Your rental management system is ready for deployment!")
    else:
        print("\n🔧 SMS test failed. Please check:")
        print("1. Your Africa's Talking account credentials")
        print("2. Account verification status")
        print("3. Available credits")
        print("4. Phone number format")


if __name__ == "__main__":
    main()