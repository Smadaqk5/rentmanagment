#!/usr/bin/env python
"""
Generate a secure SECRET_KEY for Django
"""

import secrets
import string


def generate_secret_key():
    """Generate a secure Django SECRET_KEY"""
    # Django SECRET_KEY should be at least 50 characters
    # and contain a mix of letters, digits, and symbols
    
    # Generate a random string with letters, digits, and symbols
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
    
    return secret_key


def main():
    """Generate and display SECRET_KEY"""
    print("🔐 Django SECRET_KEY Generator")
    print("=" * 40)
    
    # Generate the key
    secret_key = generate_secret_key()
    
    print(f"✅ Your SECRET_KEY:")
    print(f"SECRET_KEY = {secret_key}")
    
    print(f"\n📋 Copy this to your Heroku Config Vars:")
    print(f"SECRET_KEY = {secret_key}")
    
    print(f"\n⚠️  Important Security Notes:")
    print(f"• Keep this key secret and secure")
    print(f"• Never commit it to version control")
    print(f"• Use different keys for development and production")
    print(f"• If compromised, generate a new one immediately")
    
    print(f"\n🎯 Next Steps:")
    print(f"1. Copy the SECRET_KEY above")
    print(f"2. Go to your Heroku app dashboard")
    print(f"3. Settings → Config Vars")
    print(f"4. Add SECRET_KEY with the value above")
    print(f"5. Deploy your app")


if __name__ == "__main__":
    main()
