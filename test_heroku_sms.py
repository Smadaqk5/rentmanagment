#!/usr/bin/env python
"""
Test SMS functionality on Heroku to diagnose the 500 error
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


def test_heroku_sms():
    """Test SMS functionality on Heroku"""
    print("🔍 Testing Heroku SMS Functionality")
    print("=" * 45)
    
    try:
        # Initialize SMS service
        sms_service = AfricasTalkingService()
        
        print(f"✅ SMS service initialized")
        print(f"✅ Username: {sms_service.username}")
        print(f"✅ Sender ID: {sms_service.sender_id}")
        print(f"✅ API Key: {'*' * len(sms_service.api_key) if sms_service.api_key else 'Not set'}")
        
        # Test connection
        success, message = sms_service.test_connection()
        if success:
            print(f"✅ Connection test: {message}")
        else:
            print(f"❌ Connection test: {message}")
            return False
        
        # Test with a real phone number
        test_phone = input("\nEnter a real phone number to test SMS (e.g., 0712345678): ").strip()
        if not test_phone:
            print("❌ Phone number is required!")
            return False
        
        test_message = "Test SMS from Heroku - Rental Management System"
        
        print(f"\n📤 Sending test SMS to: {test_phone}")
        print(f"📝 Message: {test_message}")
        
        # Send SMS
        success, message = sms_service.send_sms(test_phone, test_message)
        
        if success:
            print(f"✅ {message}")
            return True
        else:
            print(f"❌ {message}")
            return False
            
    except Exception as e:
        print(f"❌ SMS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bulk_sms_simulation():
    """Simulate bulk SMS functionality"""
    print("\n🔍 Testing Bulk SMS Simulation")
    print("=" * 40)
    
    try:
        # Get tenants
        tenants = Tenant.objects.all()
        print(f"👥 Total tenants: {tenants.count()}")
        
        if tenants.count() == 0:
            print("❌ No tenants found!")
            return False
        
        # Test SMS for each tenant
        sms_service = AfricasTalkingService()
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
        print(f"❌ Bulk SMS simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_sms_logs():
    """Check SMS logs for errors"""
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
    print("🚀 Heroku SMS Diagnostic Tool")
    print("=" * 60)
    
    print("This will test SMS functionality on Heroku to diagnose the 500 error.")
    print("Make sure you're running this on Heroku or with Heroku environment variables.")
    
    # Check SMS logs
    logs_exist = check_sms_logs()
    
    # Test individual SMS
    individual_ok = test_heroku_sms()
    
    # Test bulk SMS simulation
    if individual_ok:
        bulk_ok = test_bulk_sms_simulation()
    else:
        bulk_ok = False
    
    # Summary
    print("\n📊 SMS Status Summary")
    print("=" * 30)
    print(f"SMS Logs: {'✅' if logs_exist else '❌'}")
    print(f"Individual SMS: {'✅' if individual_ok else '❌'}")
    print(f"Bulk SMS: {'✅' if bulk_ok else '❌'}")
    
    if individual_ok and bulk_ok:
        print("\n🎉 SMS functionality is working!")
        print("✅ The 500 error should be fixed")
    else:
        print("\n🔧 Issues found:")
        if not individual_ok:
            print("   - Individual SMS failed")
        if not bulk_ok:
            print("   - Bulk SMS failed")
        
        print("\n💡 Troubleshooting steps:")
        print("1. Check Africa's Talking account status")
        print("2. Verify API credentials")
        print("3. Check account credits")
        print("4. Test with real phone numbers")
        print("5. Check Heroku logs for specific errors")


if __name__ == "__main__":
    main()
