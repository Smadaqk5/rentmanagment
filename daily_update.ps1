# Daily Payment Status Update Script
Set-Location "C:\Users\File!!\Desktop\MANAGE RENT"
& "venv\Scripts\Activate.ps1"
python manage.py update_payment_status
Write-Host "Payment status update completed at $(Get-Date)"
