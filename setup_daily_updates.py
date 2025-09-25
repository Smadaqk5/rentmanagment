#!/usr/bin/env python
"""
Setup script for daily payment status updates
This script helps set up automatic daily updates for payment statuses
"""

import os
import sys
from pathlib import Path

def create_batch_file():
    """Create a Windows batch file for daily updates"""
    batch_content = """@echo off
cd /d "C:\\Users\\File!!\\Desktop\\MANAGE RENT"
call venv\\Scripts\\activate
python manage.py update_payment_status
echo Payment status update completed at %date% %time%
"""
    
    with open('daily_update.bat', 'w') as f:
        f.write(batch_content)
    
    print("✓ Created daily_update.bat file")
    print("  You can run this manually or set it up as a Windows Task Scheduler job")

def create_powershell_script():
    """Create a PowerShell script for daily updates"""
    ps_content = """# Daily Payment Status Update Script
Set-Location "C:\\Users\\File!!\\Desktop\\MANAGE RENT"
& "venv\\Scripts\\Activate.ps1"
python manage.py update_payment_status
Write-Host "Payment status update completed at $(Get-Date)"
"""
    
    with open('daily_update.ps1', 'w') as f:
        f.write(ps_content)
    
    print("✓ Created daily_update.ps1 file")
    print("  You can run this manually or set it up as a Windows Task Scheduler job")

def show_instructions():
    """Show setup instructions"""
    print("\n" + "="*60)
    print("DAILY PAYMENT STATUS UPDATE SETUP")
    print("="*60)
    print("\nTo set up automatic daily updates:")
    print("\n1. WINDOWS TASK SCHEDULER:")
    print("   - Open Task Scheduler")
    print("   - Create Basic Task")
    print("   - Name: 'Rental Management Daily Update'")
    print("   - Trigger: Daily at 6:00 AM")
    print("   - Action: Start a program")
    print("   - Program: C:\\Users\\File!!\\Desktop\\MANAGE RENT\\daily_update.bat")
    print("\n2. MANUAL EXECUTION:")
    print("   - Run: daily_update.bat")
    print("   - Or: daily_update.ps1")
    print("\n3. COMMAND LINE:")
    print("   - Activate virtual environment")
    print("   - Run: python manage.py update_payment_status")
    print("\n4. MONTHLY RESET:")
    print("   - Run: python manage.py reset_monthly_rent --confirm")
    print("   - This resets all paid tenants for the new month")
    print("\n" + "="*60)

def main():
    print("Setting up daily payment status updates...")
    
    # Create batch and PowerShell files
    create_batch_file()
    create_powershell_script()
    
    # Show instructions
    show_instructions()
    
    print("\n✓ Setup completed!")
    print("✓ Daily update scripts created")
    print("✓ Ready for automatic payment status updates")

if __name__ == "__main__":
    main()
