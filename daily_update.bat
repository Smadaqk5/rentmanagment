@echo off
cd /d "C:\Users\File!!\Desktop\MANAGE RENT"
call venv\Scripts\activate
python manage.py update_payment_status
echo Payment status update completed at %date% %time%
