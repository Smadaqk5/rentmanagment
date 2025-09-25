#!/usr/bin/env python
"""
Test script for Africa's Talking SMS integration
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


def test_africas_talking():
    """Test Africa's Talking SMS service"""
    print("🧪 Testing Africa's Talking SMS Service")
    print("=" * 50)
    
    # Initialize service
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
        "+254712345678",
        "712345678"
    ]
    
    for number in test_numbers:
        formatted = sms_service._format_phone_number(number)
        print(f"   {number} → {formatted}")
    
    # Test SMS sending (with dummy data)
    print("\n3. Testing SMS sending...")
    test_phone = "+254700000000"  # Dummy number
    test_message = "Test message from Rental Management System"
    
    print(f"   Sending to: {test_phone}")
    print(f"   Message: {test_message}")
    
    success, message = sms_service.send_sms(test_phone, test_message)
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    # Test statistics
    print("\n4. Testing SMS statistics...")
    stats = sms_service.get_sms_statistics()
    print(f"   Total SMS: {stats.get('total_sms', 0)}")
    print(f"   Successful: {stats.get('successful_sms', 0)}")
    print(f"   Failed: {stats.get('failed_sms', 0)}")
    print(f"   Success Rate: {stats.get('success_rate', 0):.1f}%")
    
    print("\n🎉 Africa's Talking test completed!")
    return True


def setup_africas_talking():
    """Setup Africa's Talking configuration"""
    print("🔧 Setting up Africa's Talking configuration...")
    
    # Get user input
    username = input("Enter your Africa's Talking username (or 'sandbox' for testing): ").strip()
    if not username:
        username = "sandbox"
    
    api_key = input("Enter your Africa's Talking API key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        return False
    
    sender_id = input("Enter your sender ID (or 'RENTAL' for default): ").strip()
    if not sender_id:
        sender_id = "RENTAL"
    
    # Update .env file
    env_file = Path(".env")
    if env_file.exists():
        # Read existing .env file
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Update or add Africa's Talking configuration
        lines = content.split('\n')
        updated_lines = []
        africas_talking_found = False
        
        for line in lines:
            if line.startswith('AFRICASTALKING_USERNAME='):
                updated_lines.append(f'AFRICASTALKING_USERNAME={username}')
                africas_talking_found = True
            elif line.startswith('AFRICASTALKING_API_KEY='):
                updated_lines.append(f'AFRICASTALKING_API_KEY={api_key}')
                africas_talking_found = True
            elif line.startswith('AFRICASTALKING_SENDER_ID='):
                updated_lines.append(f'AFRICASTALKING_SENDER_ID={sender_id}')
                africas_talking_found = True
            else:
                updated_lines.append(line)
        
        # Add Africa's Talking configuration if not found
        if not africas_talking_found:
            updated_lines.extend([
                '',
                '# Africa\'s Talking SMS Configuration',
                f'AFRICASTALKING_USERNAME={username}',
                f'AFRICASTALKING_API_KEY={api_key}',
                f'AFRICASTALKING_SENDER_ID={sender_id}'
            ])
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ .env file updated with Africa's Talking configuration")
    else:
        # Create new .env file
        env_content = f"""# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Africa's Talking SMS Configuration
AFRICASTALKING_USERNAME={username}
AFRICASTALKING_API_KEY={api_key}
AFRICASTALKING_SENDER_ID={sender_id}
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created with Africa's Talking configuration")
    
    return True


def main():
    """Main function"""
    print("🚀 Africa's Talking SMS Setup for Rental Management System")
    print("=" * 60)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("📝 No .env file found. Let's create one...")
        if not setup_africas_talking():
            return
    
    # Test the service
    test_africas_talking()
    
    print("\n📋 Next steps:")
    print("1. Get your Africa's Talking API credentials from https://africastalking.com")
    print("2. Update your .env file with the correct credentials")
    print("3. Test the SMS functionality in your Django app")
    print("4. Deploy your application")


if __name__ == "__main__":
    main()
