from django.contrib import admin
from .models import Tenant, Payment, SMSLog


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'apartment_number', 'phone', 'rent_amount_display', 'amount_due_display', 'due_date', 'rent_status', 'created_at']
    list_filter = ['rent_status', 'created_at', 'due_date']
    search_fields = ['name', 'apartment_number', 'phone']
    list_editable = ['rent_status', 'due_date']
    
    def rent_amount_display(self, obj):
        return f"KSh {obj.rent_amount}"
    rent_amount_display.short_description = 'Rent Amount'
    
    def amount_due_display(self, obj):
        return f"KSh {obj.amount_due}"
    amount_due_display.short_description = 'Amount Due'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'amount_display', 'payment_type', 'date', 'status']
    list_filter = ['status', 'payment_type', 'date']
    search_fields = ['tenant__name', 'notes']
    
    def amount_display(self, obj):
        return f"KSh {obj.amount}"
    amount_display.short_description = 'Amount'


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'status', 'sent_at', 'message_preview']
    list_filter = ['status', 'sent_at']
    search_fields = ['tenant__name', 'message']
    readonly_fields = ['sent_at', 'response_data']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'
