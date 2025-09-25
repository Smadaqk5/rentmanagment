import requests
import json
from django.conf import settings
from django.contrib import messages


class WhatsAppService:
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
    
    def send_message(self, to_phone, message):
        """Send a WhatsApp message to a phone number"""
        if not self.access_token or not self.phone_number_id:
            return False, "WhatsApp API not configured"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {
                "body": message
            }
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            if response.status_code == 200:
                return True, "Message sent successfully"
            else:
                return False, f"Failed to send message: {response.text}"
        except Exception as e:
            return False, f"Error sending message: {str(e)}"
    
    def send_rent_confirmation(self, tenant):
        """Send rent payment confirmation message"""
        message = f"Hello {tenant.name}, we have received your rent payment for apartment {tenant.apartment_number}. Thank you!"
        return self.send_message(tenant.phone, message)
    
    def send_rent_reminder(self, tenant):
        """Send rent reminder message"""
        message = f"Hello {tenant.name}, this is a friendly reminder that your rent for apartment {tenant.apartment_number} (KSh {tenant.rent_amount}) is due. Please make your payment as soon as possible. Thank you!"
        return self.send_message(tenant.phone, message)
