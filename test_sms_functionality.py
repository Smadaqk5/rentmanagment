#!/usr/bin/env python
"""
Test SMS functionality and diagnose issues
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
from rental_app.models import Tenant, SMSLog


def check_sms_environment():
    """Check SMS environment variables"""
    print("🔍 Checking SMS Environment Variables")
    print("=" * 50)
    
    required_vars = {
        'AFRICASTALKING_USERNAME': 'Africa\'s Talking username',
        'AFRICASTALKING_API_KEY': 'Africa\'s Talking API key',
        'AFRICASTALKING_SENDER_ID': 'SMS sender ID'
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            if var == 'AFRICASTALKING_API_KEY':
                print(f"✅ {var}: {'*' * len(value)} ({description})")
            else:
                print(f"✅ {var}: {value} ({description})")
        else:
            print(f"❌ {var}: Not set ({description})")
            missing_vars.append(var)
    
    return len(missing_vars) == 0


def test_sms_service():
    """Test SMS service initialization"""
    print("\n🔍 Testing SMS Service")
    print("=" * 30)
    
    try:
        sms_service = AfricasTalkingService()
        
        print(f"✅ SMS service initialized")
        print(f"✅ Username: {sms_service.username}")
        print(f"✅ Sender ID: {sms_service.sender_id}")
        print(f"✅ API Key configured: {'✅' if sms_service.api_key else '❌'}")
        
        return sms_service
        
    except Exception as e:
        print(f"❌ SMS service initialization failed: {e}")
        return None


def test_phone_number_formatting(sms_service):
    """Test phone number formatting"""
    print("\n🔍 Testing Phone Number Formatting")
    print("=" * 40)
    
    test_numbers = [
        "0712345678",
        "254712345678", 
        "+254712345678",
        "712345678"
    ]
    
    for number in test_numbers:
        try:
            formatted = sms_service._format_phone_number(number)
            print(f"✅ {number} → {formatted}")
        except Exception as e:
            print(f"❌ {number} → Error: {e}")


def test_sms_connection(sms_service):
    """Test SMS connection"""
    print("\n🔍 Testing SMS Connection")
    print("=" * 30)
    
    try:
        success, message = sms_service.test_connection()
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


def test_sms_sending(sms_service):
    """Test SMS sending with dummy data"""
    print("\n🔍 Testing SMS Sending")
    print("=" * 30)
    
    # Use a dummy number for testing
    test_phone = "+254700000000"
    test_message = "Test message from Rental Management System"
    
    print(f"📤 Sending test SMS to: {test_phone}")
    print(f"📝 Message: {test_message}")
    
    try:
        success, message = sms_service.send_sms(test_phone, test_message)
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
    except Exception as e:
        print(f"❌ SMS sending failed: {e}")
        return False


def check_sms_logs():
    """Check SMS logs in database"""
    print("\n🔍 Checking SMS Logs")
    print("=" * 25)
    
    try:
        total_sms = SMSLog.objects.count()
        successful_sms = SMSLog.objects.filter(status='success').count()
        failed_sms = SMSLog.objects.filter(status='failure').count()
        
        print(f"📊 Total SMS attempts: {total_sms}")
        print(f"✅ Successful SMS: {successful_sms}")
        print(f"❌ Failed SMS: {failed_sms}")
        
        if total_sms > 0:
            success_rate = (successful_sms / total_sms) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
            
            # Show recent SMS logs
            recent_logs = SMSLog.objects.order_by('-sent_at')[:5]
            print(f"\n📋 Recent SMS logs:")
            for log in recent_logs:
                status_icon = "✅" if log.status == 'success' else "❌"
                print(f"   {status_icon} {log.tenant.name if log.tenant else 'Test'} - {log.status} - {log.sent_at.strftime('%Y-%m-%d %H:%M')}")
        
        return total_sms > 0
        
    except Exception as e:
        print(f"❌ Error checking SMS logs: {e}")
        return False


def check_tenants():
    """Check if there are tenants to send SMS to"""
    print("\n🔍 Checking Tenants")
    print("=" * 20)
    
    try:
        total_tenants = Tenant.objects.count()
        tenants_with_phone = Tenant.objects.exclude(phone='').count()
        
        print(f"👥 Total tenants: {total_tenants}")
        print(f"📱 Tenants with phone: {tenants_with_phone}")
        
        if tenants_with_phone > 0:
            print(f"\n📋 Tenants with phone numbers:")
            for tenant in Tenant.objects.exclude(phone='')[:5]:
                print(f"   • {tenant.name}: {tenant.phone}")
        
        return tenants_with_phone > 0
        
    except Exception as e:
        print(f"❌ Error checking tenants: {e}")
        return False


def main():
    """Main SMS diagnostic function"""
    print("🚀 SMS Functionality Diagnostic Tool")
    print("=" * 60)
    
    # Check environment variables
    env_ok = check_sms_environment()
    
    if not env_ok:
        print("\n❌ Missing SMS environment variables!")
        print("💡 Please set these in your Heroku Config Vars:")
        print("   AFRICASTALKING_USERNAME=smadaqk5")
        print("   AFRICASTALKING_API_KEY=atsk_0d6f9d0aabc3a50368896f809414ec0ad6909bf7c1dadeb65cf964e2423995cca9c2db28")
        print("   AFRICASTALKING_SENDER_ID=RENTAL")
        return
    
    # Test SMS service
    sms_service = test_sms_service()
    if not sms_service:
        return
    
    # Test phone number formatting
    test_phone_number_formatting(sms_service)
    
    # Test SMS connection
    connection_ok = test_sms_connection(sms_service)
    
    # Test SMS sending
    if connection_ok:
        sending_ok = test_sms_sending(sms_service)
    else:
        sending_ok = False
    
    # Check SMS logs
    logs_exist = check_sms_logs()
    
    # Check tenants
    tenants_exist = check_tenants()
    
    # Summary
    print("\n📊 SMS Status Summary")
    print("=" * 30)
    print(f"Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"SMS Service: {'✅' if sms_service else '❌'}")
    print(f"Connection: {'✅' if connection_ok else '❌'}")
    print(f"SMS Sending: {'✅' if sending_ok else '❌'}")
    print(f"SMS Logs: {'✅' if logs_exist else '❌'}")
    print(f"Tenants: {'✅' if tenants_exist else '❌'}")
    
    if env_ok and sms_service and connection_ok and sending_ok:
        print("\n🎉 SMS functionality is working!")
        print("✅ You can send SMS reminders to tenants")
    else:
        print("\n🔧 Issues found:")
        if not env_ok:
            print("   - Missing environment variables")
        if not sms_service:
            print("   - SMS service initialization failed")
        if not connection_ok:
            print("   - Cannot connect to Africa's Talking API")
        if not sending_ok:
            print("   - SMS sending failed")
        if not tenants_exist:
            print("   - No tenants with phone numbers")
        
        print("\n💡 Troubleshooting steps:")
        print("1. Check Africa's Talking account status")
        print("2. Verify API credentials")
        print("3. Check account credits")
        print("4. Test with real phone numbers")
        print("5. Check SMS logs for error details")


if __name__ == "__main__":
    main()
