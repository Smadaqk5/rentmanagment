#!/usr/bin/env python
"""
Test script for SMSMobile API integration
Run this to test if the SMS API is working correctly
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_management.settings')
django.setup()

from rental_app.sms_service import SMSMobileService

def test_sms_api():
    """Test the SMSMobile API"""
    print("🧪 Testing SMSMobile API Integration")
    print("=" * 50)
    
    # Initialize SMS service
    sms = SMSMobileService()
    
    # Test phone number (replace with your own for testing)
    test_phone = "+254700000000"  # Replace with a real number for testing
    test_message = "Hello! This is a test message from your Rental Management System. If you receive this, the SMS integration is working correctly!"
    
    print(f"📱 Sending test SMS to: {test_phone}")
    print(f"📝 Message: {test_message}")
    print()
    
    # Send test SMS
    success, result_message = sms.send_sms(test_phone, test_message)
    
    if success:
        print("✅ SMS sent successfully!")
        print(f"📋 Result: {result_message}")
    else:
        print("❌ SMS failed!")
        print(f"📋 Error: {result_message}")
    
    print()
    print("🔧 Configuration Check:")
    print(f"   API Key: {'✅ Set' if sms.api_key else '❌ Missing'}")
    print(f"   API URL: {sms.api_url}")
    print(f"   Sender ID: {sms.sender_id}")
    
    print()
    print("📊 SMS Statistics:")
    stats = sms.get_sms_statistics()
    print(f"   Total SMS sent: {stats['total_sent']}")
    print(f"   Success rate: {stats['success_rate']}%")
    print(f"   Successful: {stats['success_count']}")
    print(f"   Failed: {stats['failure_count']}")

if __name__ == "__main__":
    test_sms_api()
