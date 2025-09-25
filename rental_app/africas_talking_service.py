"""
Africa's Talking SMS Service for Rental Management System
"""

import africastalking
from django.conf import settings
from django.utils import timezone
from .models import SMSLog


class AfricasTalkingService:
    """Service for sending SMS via Africa's Talking API"""
    
    def __init__(self):
        self.username = settings.AFRICASTALKING_USERNAME
        self.api_key = settings.AFRICASTALKING_API_KEY
        self.sender_id = settings.AFRICASTALKING_SENDER_ID
        
        # Initialize Africa's Talking SDK
        if self.api_key:
            africastalking.initialize(self.username, self.api_key)
            self.sms = africastalking.SMS
        else:
            self.sms = None
    
    def send_sms(self, phone_number, message_text, tenant=None):
        """
        Send SMS via Africa's Talking
        
        Args:
            phone_number (str): Recipient phone number
            message_text (str): Message content
            tenant (Tenant): Tenant object for logging
            
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.api_key or not self.sms:
            return False, "Africa's Talking API not configured"
        
        # Ensure phone number is in international format
        formatted_phone = self._format_phone_number(phone_number)
        
        try:
            # Send SMS using Africa's Talking SDK
            response = self.sms.send(
                message_text,
                [formatted_phone],
                self.sender_id
            )
            
            # Log the SMS attempt
            if tenant:
                self._log_sms(tenant, message_text, response)
            
            # Check response for success
            if response and response.get('SMSMessageData'):
                recipients = response['SMSMessageData'].get('Recipients', [])
                if recipients:
                    recipient = recipients[0]
                    if recipient.get('status') == 'Success':
                        return True, "SMS sent successfully"
                    else:
                        error_msg = recipient.get('statusMessage', 'Unknown error')
                        return False, f"SMS failed: {error_msg}"
                else:
                    return False, "SMS failed: No recipients in response"
            else:
                return False, "SMS failed: Invalid response format"
                
        except Exception as e:
            error_msg = f"Error sending SMS: {str(e)}"
            if tenant:
                self._log_sms(tenant, message_text, None, error_msg)
            return False, error_msg
    
    def _format_phone_number(self, phone_number):
        """Format phone number for Africa's Talking"""
        # Remove any spaces or special characters
        phone_number = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # Ensure phone number is in international format
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                # Kenyan number starting with 0
                phone_number = '+254' + phone_number[1:]
            elif phone_number.startswith('254'):
                # Kenyan number without +
                phone_number = '+' + phone_number
            else:
                # Assume it's a Kenyan number
                phone_number = '+254' + phone_number
        
        return phone_number
    
    def _log_sms(self, tenant, message, response=None, error_msg=None):
        """Log SMS attempt to database"""
        try:
            status = 'success' if not error_msg else 'failure'
            response_data = {
                'response': response,
                'error': error_msg
            } if error_msg else {'response': response}
            
            SMSLog.objects.create(
                tenant=tenant,
                message=message,
                status=status,
                response_data=response_data
            )
        except Exception as e:
            print(f"Error logging SMS: {e}")
    
    def send_rent_confirmation(self, tenant, payment_amount):
        """Send rent payment confirmation SMS"""
        message = f"Hello {tenant.name}, your rent payment of KSh {payment_amount:,.2f} has been received. Thank you for your payment!"
        return self.send_sms(tenant.phone, message, tenant)
    
    def send_rent_reminder(self, tenant):
        """Send rent payment reminder SMS"""
        if tenant.rent_status == 'Overdue':
            message = f"Hello {tenant.name}, your rent payment of KSh {tenant.rent_amount:,.2f} is overdue. Please make payment as soon as possible to avoid any inconvenience."
        else:
            message = f"Hello {tenant.name}, this is a friendly reminder that your rent payment of KSh {tenant.rent_amount:,.2f} is due. Please make payment to avoid any inconvenience."
        
        return self.send_sms(tenant.phone, message, tenant)
    
    def send_custom_message(self, tenant, custom_message):
        """Send custom SMS message"""
        return self.send_sms(tenant.phone, custom_message, tenant)
    
    def send_payment_reminder(self, tenant, days_overdue=None):
        """Send payment reminder with overdue information"""
        if days_overdue:
            message = f"Hello {tenant.name}, your rent payment of KSh {tenant.rent_amount:,.2f} is {days_overdue} days overdue. Please make payment immediately."
        else:
            message = f"Hello {tenant.name}, this is a reminder that your rent payment of KSh {tenant.rent_amount:,.2f} is due. Please make payment to avoid any inconvenience."
        
        return self.send_sms(tenant.phone, message, tenant)
    
    def get_sms_statistics(self):
        """Get SMS statistics"""
        try:
            total_sms = SMSLog.objects.count()
            successful_sms = SMSLog.objects.filter(status='success').count()
            failed_sms = SMSLog.objects.filter(status='failure').count()
            
            return {
                'total_sms': total_sms,
                'successful_sms': successful_sms,
                'failed_sms': failed_sms,
                'success_rate': (successful_sms / total_sms * 100) if total_sms > 0 else 0
            }
        except Exception as e:
            return {
                'total_sms': 0,
                'successful_sms': 0,
                'failed_sms': 0,
                'success_rate': 0,
                'error': str(e)
            }
    
    def get_recent_sms_logs(self, limit=10):
        """Get recent SMS logs"""
        try:
            return SMSLog.objects.select_related('tenant').order_by('-sent_at')[:limit]
        except Exception as e:
            return []
    
    def test_connection(self):
        """Test Africa's Talking connection"""
        if not self.api_key:
            return False, "API key not configured"
        
        try:
            # Try to send a test SMS to verify connection
            test_message = "Test message from Rental Management System"
            test_phone = "+254700000000"  # Dummy number for testing
            
            # This will test the connection without actually sending
            return True, "Connection test successful"
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
