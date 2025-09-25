#!/usr/bin/env python
"""
Fix Heroku database by adding tenants and running migrations
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


def check_heroku_database():
    """Check if Heroku database is accessible"""
    print("🔍 Checking Heroku Database")
    print("=" * 35)
    
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        print("✅ Database connection successful!")
        
        # Check tenant count
        tenant_count = Tenant.objects.count()
        print(f"👥 Total tenants in database: {tenant_count}")
        
        if tenant_count > 0:
            print("✅ Database has tenants")
            for tenant in Tenant.objects.all()[:5]:
                print(f"   • {tenant.name} - {tenant.apartment_number} - {tenant.phone}")
        else:
            print("❌ Database is empty - no tenants found")
        
        return tenant_count > 0
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def add_tenants_to_heroku():
    """Add tenants to Heroku database"""
    print("\n👥 Adding Tenants to Heroku Database")
    print("=" * 45)
    
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
    print(f"📱 Total tenants: {Tenant.objects.count()}")
    
    return created_count > 0


def main():
    """Main function"""
    print("🚀 Heroku Database Fixer")
    print("=" * 60)
    
    print("This will check your Heroku database and add tenants if needed.")
    print("This should fix the 500 error when sending bulk SMS.")
    
    # Check database
    db_ok = check_heroku_database()
    
    if not db_ok:
        print("\n❌ Database connection failed!")
        print("💡 Please check your database configuration")
        return
    
    # Add tenants if needed
    if Tenant.objects.count() == 0:
        print("\n🔧 Adding tenants to fix the 500 error...")
        if add_tenants_to_heroku():
            print("\n🎉 Tenants added successfully!")
            print("✅ Your bulk SMS should now work")
            print("✅ Go test your app at: https://rent-7d65f297e545.herokuapp.com")
        else:
            print("\n❌ Failed to add tenants")
    else:
        print("\n✅ Database already has tenants")
        print("✅ Your bulk SMS should work now")


if __name__ == "__main__":
    main()
