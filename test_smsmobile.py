#!/usr/bin/env python
"""
Test SMSMobile API functionality
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

from rental_app.sms_service import SMSMobileService
from rental_app.models import Tenant, SMSLog


def test_smsmobile_configuration():
    """Test SMSMobile configuration"""
    print("🔍 Testing SMSMobile Configuration")
    print("=" * 45)
    
    try:
        sms_service = SMSMobileService()
        
        print(f"✅ SMSMobile service initialized")
        print(f"✅ API Key: {'*' * len(sms_service.api_key) if sms_service.api_key else 'Not set'}")
        print(f"✅ API URL: {sms_service.api_url}")
        print(f"✅ Sender ID: {sms_service.sender_id}")
        
        return sms_service
        
    except Exception as e:
        print(f"❌ SMSMobile service initialization failed: {e}")
        return None


def test_smsmobile_sms():
    """Test SMSMobile SMS sending"""
    print("\n🔍 Testing SMSMobile SMS Sending")
    print("=" * 40)
    
    # Get phone number from user
    phone_number = input("Enter a real phone number to test SMS (e.g., 0712345678): ").strip()
    if not phone_number:
        print("❌ Phone number is required!")
        return False
    
    try:
        sms_service = SMSMobileService()
        
        # Test message
        test_message = "Test SMS from SMSMobile API - Rental Management System"
        
        print(f"\n📤 Sending SMS to: {phone_number}")
        print(f"📝 Message: {test_message}")
        print(f"👤 Sender ID: {sms_service.sender_id}")
        
        # Send SMS
        success, message = sms_service.send_sms(phone_number, test_message)
        
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
            
    except Exception as e:
        print(f"❌ SMSMobile SMS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bulk_smsmobile():
    """Test bulk SMS with SMSMobile"""
    print("\n🔍 Testing Bulk SMS with SMSMobile")
    print("=" * 45)
    
    try:
        # Get tenants
        tenants = Tenant.objects.all()
        print(f"👥 Total tenants: {tenants.count()}")
        
        if tenants.count() == 0:
            print("❌ No tenants found!")
            return False
        
        sms_service = SMSMobileService()
        success_count = 0
        failure_count = 0
        
        for tenant in tenants:
            if tenant.phone:
                print(f"\n📱 Testing SMS for {tenant.name} ({tenant.phone})")
                
                try:
                    # Test SMS sending
                    success, message = sms_service.send_sms(
                        tenant.phone, 
                        f"Test bulk SMS for {tenant.name}",
                        tenant
                    )
                    
                    if success:
                        print(f"✅ {message}")
                        success_count += 1
                    else:
                        print(f"❌ {message}")
                        failure_count += 1
                        
                except Exception as e:
                    print(f"❌ Error sending SMS to {tenant.name}: {e}")
                    failure_count += 1
            else:
                print(f"⚠️  {tenant.name} has no phone number")
        
        print(f"\n📊 Bulk SMS Results:")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failure_count}")
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Bulk SMSMobile test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_sms_logs():
    """Check SMS logs"""
    print("\n🔍 Checking SMS Logs")
    print("=" * 25)
    
    try:
        total_sms = SMSLog.objects.count()
        successful_sms = SMSLog.objects.filter(status='success').count()
        failed_sms = SMSLog.objects.filter(status='failure').count()
        
        print(f"📊 Total SMS attempts: {total_sms}")
        print(f"✅ Successful SMS: {successful_sms}")
        print(f"❌ Failed SMS: {failed_sms}")
        
        if failed_sms > 0:
            print(f"\n❌ Recent failed SMS:")
            failed_logs = SMSLog.objects.filter(status='failure').order_by('-sent_at')[:5]
            for log in failed_logs:
                print(f"   • {log.tenant.name if log.tenant else 'Unknown'}: {log.response_data}")
        
        return total_sms > 0
        
    except Exception as e:
        print(f"❌ Error checking SMS logs: {e}")
        return False


def main():
    """Main function"""
    print("🚀 SMSMobile API Test Tool")
    print("=" * 60)
    
    print("This will test SMSMobile API functionality.")
    print("Make sure your SMSMobile environment variables are set correctly.")
    
    # Test configuration
    sms_service = test_smsmobile_configuration()
    if not sms_service:
        print("\n❌ SMSMobile configuration failed!")
        return
    
    # Test individual SMS
    individual_ok = test_smsmobile_sms()
    
    # Test bulk SMS
    if individual_ok:
        bulk_ok = test_bulk_smsmobile()
    else:
        bulk_ok = False
    
    # Check SMS logs
    logs_exist = check_sms_logs()
    
    # Summary
    print("\n📊 SMSMobile Status Summary")
    print("=" * 40)
    print(f"Configuration: {'✅' if sms_service else '❌'}")
    print(f"Individual SMS: {'✅' if individual_ok else '❌'}")
    print(f"Bulk SMS: {'✅' if bulk_ok else '❌'}")
    print(f"SMS Logs: {'✅' if logs_exist else '❌'}")
    
    if sms_service and individual_ok and bulk_ok:
        print("\n🎉 SMSMobile API is working perfectly!")
        print("✅ Your bulk SMS should work now")
        print("✅ The 500 error should be fixed")
    else:
        print("\n🔧 Issues found:")
        if not sms_service:
            print("   - SMSMobile configuration failed")
        if not individual_ok:
            print("   - Individual SMS failed")
        if not bulk_ok:
            print("   - Bulk SMS failed")
        
        print("\n💡 Troubleshooting steps:")
        print("1. Check SMSMobile API credentials")
        print("2. Verify API URL is correct")
        print("3. Test with real phone numbers")
        print("4. Check SMSMobile account status")


if __name__ == "__main__":
    main()
