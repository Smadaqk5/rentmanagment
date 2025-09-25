import requests
import json
from django.conf import settings
from django.contrib import messages
from .models import SMSLog, Tenant


class SMSMobileService:
    def __init__(self):
        self.api_key = settings.SMSMOBILE_API_KEY
        self.api_url = settings.SMSMOBILE_API_URL
        self.sender_id = getattr(settings, 'SMSMOBILE_SENDER_ID', 'RENTAL')
    
    def send_sms(self, phone_number, message_text, tenant=None):
        """
        Send SMS using SMSMobile API
        
        Args:
            phone_number (str): Phone number in international format (+254...)
            message_text (str): Message content
            tenant (Tenant): Tenant object for logging (optional)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.api_key or not self.api_url:
            return False, "SMSMobile API not configured"
        
        # Ensure phone number is in international format
        if not phone_number.startswith('+'):
            if phone_number.startswith('0'):
                # Convert 07... to +2547...
                phone_number = '+254' + phone_number[1:]
            elif phone_number.startswith('254'):
                # Convert 2547... to +2547...
                phone_number = '+' + phone_number
            else:
                phone_number = '+254' + phone_number
        
        # SMSMobile API uses GET requests with query parameters
        params = {
            "api_key": self.api_key,
            "recipients": phone_number,
            "message": message_text,
            "sender_id": self.sender_id
        }
        
        try:
            # Make API request using GET with query parameters
            response = requests.get(
                self.api_url,
                params=params,
                timeout=30
            )
            
            # Log the SMS attempt
            if tenant:
                self._log_sms(tenant, message_text, response)
            
            # Check response status
            if response.status_code == 200:
                response_text = response.text.strip()
                
                # SMSMobile API returns text response, check for success indicators
                if ("success" in response_text.lower() or 
                    "sent" in response_text.lower() or 
                    "accepted" in response_text.lower()):
                    return True, "SMS sent successfully"
                else:
                    return False, f"SMS failed: {response_text}"
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                return False, f"SMS failed: {error_msg}"
                
        except requests.exceptions.Timeout:
            error_msg = "SMS request timed out"
            if tenant:
                self._log_sms(tenant, message_text, None, error_msg)
            return False, error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            if tenant:
                self._log_sms(tenant, message_text, None, error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            if tenant:
                self._log_sms(tenant, message_text, None, error_msg)
            return False, error_msg
    
    def _is_success_response(self, response_data):
        """
        Check if the API response indicates success
        Adjust this based on SMSMobile API response format
        """
        # Common success indicators - adjust based on actual API response
        success_indicators = ['success', 'sent', 'delivered', 'accepted']
        
        if isinstance(response_data, dict):
            status = response_data.get('status', '').lower()
            message = response_data.get('message', '').lower()
            
            return any(indicator in status or indicator in message for indicator in success_indicators)
        
        return False
    
    def _log_sms(self, tenant, message, response=None, error_msg=None):
        """
        Log SMS attempt to database
        """
        try:
            if response and response.status_code == 200:
                response_text = response.text.strip()
                # Check if response indicates success
                success = ("success" in response_text.lower() or 
                          "sent" in response_text.lower() or 
                          "accepted" in response_text.lower())
                status = 'success' if success else 'failure'
                response_data = {'response': response_text}
            else:
                response_data = {
                    'error': error_msg or f"HTTP {response.status_code if response else 'Unknown'}"
                }
                status = 'failure'
            
            SMSLog.objects.create(
                tenant=tenant,
                message=message,
                status=status,
                response_data=response_data
            )
        except Exception as e:
            # Log error but don't fail the SMS sending
            print(f"Failed to log SMS: {e}")
    
    def send_rent_reminder(self, tenant):
        """Send rent reminder SMS to tenant"""
        message = f"Hello {tenant.name}, this is a friendly reminder that your rent for apartment {tenant.apartment_number} (KSh {tenant.rent_amount}) is due on the {tenant.due_date}th. Please make your payment as soon as possible. Thank you!"
        return self.send_sms(tenant.phone, message, tenant)
    
    def send_rent_confirmation(self, tenant):
        """Send rent payment confirmation SMS"""
        message = f"Hello {tenant.name}, we have received your rent payment for apartment {tenant.apartment_number}. Thank you for your timely payment!"
        return self.send_sms(tenant.phone, message, tenant)
    
    def send_payment_reminder(self, tenant, amount_due):
        """Send payment reminder for specific amount due"""
        message = f"Hello {tenant.name}, you have an outstanding balance of KSh {amount_due} for apartment {tenant.apartment_number}. Please make your payment as soon as possible. Thank you!"
        return self.send_sms(tenant.phone, message, tenant)
    
    def send_custom_message(self, tenant, custom_message):
        """Send custom message to tenant"""
        return self.send_sms(tenant.phone, custom_message, tenant)
    
    def get_sms_logs(self, tenant=None, limit=50):
        """Get SMS logs for a tenant or all tenants"""
        if tenant:
            return SMSLog.objects.filter(tenant=tenant).order_by('-sent_at')[:limit]
        return SMSLog.objects.select_related('tenant').order_by('-sent_at')[:limit]
    
    def get_sms_statistics(self):
        """Get SMS sending statistics"""
        from django.db.models import Count, Q
        
        stats = SMSLog.objects.aggregate(
            total_sent=Count('id'),
            success_count=Count('id', filter=Q(status='success')),
            failure_count=Count('id', filter=Q(status='failure'))
        )
        
        success_rate = 0
        if stats['total_sent'] > 0:
            success_rate = (stats['success_count'] / stats['total_sent']) * 100
        
        return {
            'total_sent': stats['total_sent'],
            'success_count': stats['success_count'],
            'failure_count': stats['failure_count'],
            'success_rate': round(success_rate, 2)
        }
