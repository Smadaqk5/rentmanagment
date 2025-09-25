#!/usr/bin/env python
"""
Fix .env file to use SQLite for local development
"""

def fix_env_file():
    """Create .env file with SQLite configuration for local development"""
    env_content = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Supabase Database Configuration (Commented out for local development)
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-supabase-anon-key
# SUPABASE_DB_NAME=postgres
# SUPABASE_DB_USER=postgres
# SUPABASE_DB_PASSWORD=your-database-password
# SUPABASE_DB_HOST=db.your-project.supabase.co
# SUPABASE_DB_PORT=5432

# SMSMobile API Configuration
SMSMOBILE_API_KEY=b02fa0e9633854c45d4a1c7cc6186c9ef7e1b700f3d2b97f
SMSMOBILE_API_URL=https://api.smsmobile.africa/v1/send
SMSMOBILE_SENDER_ID=RENTAL

# WhatsApp Cloud API Configuration (Deprecated - kept for backward compatibility)
WHATSAPP_ACCESS_TOKEN=your-whatsapp-access-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_VERIFY_TOKEN=your-verify-token
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Fixed .env file to use SQLite for local development")

if __name__ == "__main__":
    fix_env_file()
    print("🎉 Environment fixed! Now using SQLite database.")
