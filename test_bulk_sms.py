#!/usr/bin/env python
"""
Test bulk SMS functionality and diagnose issues
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


def test_bulk_sms_functionality():
    """Test bulk SMS functionality"""
    print("🔍 Testing Bulk SMS Functionality")
    print("=" * 50)
    
    try:
        # Initialize SMS service
        sms_service = AfricasTalkingService()
        
        # Check if there are tenants
        tenants = Tenant.objects.all()
        print(f"👥 Total tenants: {tenants.count()}")
        
        if tenants.count() == 0:
            print("❌ No tenants found!")
            print("💡 Add some tenants first to test bulk SMS")
            return False
        
        # Test bulk SMS for each tenant
        success_count = 0
        failure_count = 0
        
        for tenant in tenants:
            if tenant.phone:
                print(f"\n📱 Testing SMS for {tenant.name} ({tenant.phone})")
                
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
            else:
                print(f"⚠️  {tenant.name} has no phone number")
        
        print(f"\n📊 Bulk SMS Results:")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Failed: {failure_count}")
        
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Bulk SMS test failed: {e}")
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


def test_sms_service_initialization():
    """Test SMS service initialization"""
    print("\n🔍 Testing SMS Service Initialization")
    print("=" * 45)
    
    try:
        sms_service = AfricasTalkingService()
        
        print(f"✅ SMS service initialized")
        print(f"✅ Username: {sms_service.username}")
        print(f"✅ Sender ID: {sms_service.sender_id}")
        print(f"✅ API Key configured: {'✅' if sms_service.api_key else '❌'}")
        
        # Test connection
        success, message = sms_service.test_connection()
        if success:
            print(f"✅ Connection test: {message}")
        else:
            print(f"❌ Connection test: {message}")
        
        return sms_service
        
    except Exception as e:
        print(f"❌ SMS service initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function"""
    print("🚀 Bulk SMS Diagnostic Tool")
    print("=" * 60)
    
    # Test SMS service initialization
    sms_service = test_sms_service_initialization()
    if not sms_service:
        print("\n❌ SMS service initialization failed!")
        return
    
    # Check SMS logs
    logs_exist = check_sms_logs()
    
    # Test bulk SMS functionality
    bulk_sms_ok = test_bulk_sms_functionality()
    
    # Summary
    print("\n📊 Bulk SMS Status Summary")
    print("=" * 40)
    print(f"SMS Service: {'✅' if sms_service else '❌'}")
    print(f"SMS Logs: {'✅' if logs_exist else '❌'}")
    print(f"Bulk SMS: {'✅' if bulk_sms_ok else '❌'}")
    
    if sms_service and bulk_sms_ok:
        print("\n🎉 Bulk SMS functionality is working!")
        print("✅ You can send bulk SMS reminders to tenants")
    else:
        print("\n🔧 Issues found:")
        if not sms_service:
            print("   - SMS service initialization failed")
        if not bulk_sms_ok:
            print("   - Bulk SMS functionality failed")
        
        print("\n💡 Troubleshooting steps:")
        print("1. Check Africa's Talking account status")
        print("2. Verify API credentials")
        print("3. Check account credits")
        print("4. Add tenants with phone numbers")
        print("5. Test individual SMS first")


if __name__ == "__main__":
    main()
