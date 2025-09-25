#!/usr/bin/env python
"""
Add sample tenants for testing
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

from rental_app.models import Tenant


def add_sample_tenants():
    """Add sample tenants for testing"""
    print("👥 Adding Sample Tenants")
    print("=" * 30)
    
    sample_tenants = [
        {
            'name': 'John Doe',
            'phone': '0712345678',
            'apartment_number': 'A1',
            'rent_amount': 15000.00,
            'rent_status': 'Unpaid'
        },
        {
            'name': 'Jane Smith',
            'phone': '0723456789',
            'apartment_number': 'A2',
            'rent_amount': 18000.00,
            'rent_status': 'Paid'
        },
        {
            'name': 'Mike Johnson',
            'phone': '0734567890',
            'apartment_number': 'B1',
            'rent_amount': 12000.00,
            'rent_status': 'Unpaid'
        },
        {
            'name': 'Sarah Wilson',
            'phone': '0745678901',
            'apartment_number': 'B2',
            'rent_amount': 20000.00,
            'rent_status': 'Unpaid'
        },
        {
            'name': 'David Brown',
            'phone': '0756789012',
            'apartment_number': 'C1',
            'rent_amount': 16000.00,
            'rent_status': 'Paid'
        }
    ]
    
    created_count = 0
    
    for tenant_data in sample_tenants:
        try:
            # Check if tenant already exists
            existing_tenant = Tenant.objects.filter(
                name=tenant_data['name'],
                apartment_number=tenant_data['apartment_number']
            ).first()
            
            if existing_tenant:
                print(f"⚠️  {tenant_data['name']} already exists")
                continue
            
            # Create new tenant
            tenant = Tenant.objects.create(
                name=tenant_data['name'],
                phone=tenant_data['phone'],
                apartment_number=tenant_data['apartment_number'],
                rent_amount=tenant_data['rent_amount'],
                rent_status=tenant_data['rent_status']
            )
            
            print(f"✅ Created: {tenant.name} - {tenant.apartment_number} - KSh {tenant.rent_amount:,.2f}")
            created_count += 1
            
        except Exception as e:
            print(f"❌ Failed to create {tenant_data['name']}: {e}")
    
    print(f"\n📊 Summary:")
    print(f"✅ Created: {created_count} tenants")
    print(f"📱 Total tenants with phone: {Tenant.objects.exclude(phone='').count()}")
    
    return created_count > 0


def main():
    """Main function"""
    print("🚀 Sample Tenants Creator")
    print("=" * 60)
    
    print("This will add sample tenants to your database for testing.")
    print("These tenants have phone numbers so you can test SMS functionality.")
    
    confirm = input("\nDo you want to add sample tenants? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Operation cancelled.")
        return
    
    if add_sample_tenants():
        print("\n🎉 Sample tenants added successfully!")
        print("✅ You can now test SMS functionality")
        print("✅ Go to your app and test bulk SMS reminders")
    else:
        print("\n❌ Failed to add sample tenants")
        print("💡 Check your database connection")


if __name__ == "__main__":
    main()
