from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

# Global constants for choices
RENT_STATUS_CHOICES = [
    ('Paid', 'Paid'),
    ('Unpaid', 'Unpaid'),
    ('Partial', 'Partial'),
    ('Overdue', 'Overdue'),
]

PAYMENT_STATUS_CHOICES = [
    ('Paid', 'Paid'),
    ('Pending', 'Pending'),
]

PAYMENT_TYPE_CHOICES = [
    ('Full', 'Full Payment'),
    ('Partial', 'Partial Payment'),
    ('Advance', 'Advance Payment'),
]


class Tenant(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)  # International format like +2547...
    apartment_number = models.CharField(max_length=50)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rent_status = models.CharField(max_length=10, choices=RENT_STATUS_CHOICES, default='Unpaid')
    due_date = models.IntegerField(default=1, help_text="Day of the month when rent is due (1-31)")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount still owed by tenant")
    last_payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - Apt {self.apartment_number}"
    
    def get_next_due_date(self):
        """Get the next due date for this tenant"""
        now = timezone.now()
        current_month = now.month
        current_year = now.year
        
        # Try to create due date for current month
        try:
            due_date = timezone.datetime(current_year, current_month, self.due_date)
            if due_date.date() < now.date():
                # Due date has passed this month, get next month
                if current_month == 12:
                    due_date = timezone.datetime(current_year + 1, 1, self.due_date)
                else:
                    due_date = timezone.datetime(current_year, current_month + 1, self.due_date)
        except ValueError:
            # Handle months with fewer days (e.g., Feb 30)
            if current_month == 12:
                due_date = timezone.datetime(current_year + 1, 1, 1)
            else:
                due_date = timezone.datetime(current_year, current_month + 1, 1)
        
        return due_date
    
    def is_overdue(self):
        """Check if the tenant's rent is overdue"""
        if self.rent_status == 'Paid':
            return False
        
        next_due = self.get_next_due_date()
        return timezone.now().date() > next_due.date()
    
    def update_status(self):
        """Update the tenant's payment status based on amount due and due date"""
        if self.amount_due <= 0:
            self.rent_status = 'Paid'
        elif self.amount_due >= self.rent_amount:
            self.rent_status = 'Unpaid'
        elif self.amount_due > 0:
            self.rent_status = 'Partial'
        
        # Check if overdue
        if self.is_overdue() and self.rent_status != 'Paid':
            self.rent_status = 'Overdue'
        
        self.save()
    
    def add_payment(self, amount):
        """Add a payment and update amount due"""
        if amount > 0:
            self.amount_due = max(0, self.amount_due - amount)
            self.last_payment_date = timezone.now()
            self.update_status()
    
    def reset_for_new_month(self):
        """Reset tenant for new month - add full rent to amount due"""
        if self.rent_status == 'Paid':
            self.amount_due = self.rent_amount
            self.rent_status = 'Unpaid'
            self.save()
    
    def delete(self, *args, **kwargs):
        """Override delete to archive tenant before deletion"""
        # Archive tenant before deletion
        ArchivedTenant.objects.create(
            original_id=self.id,
            name=self.name,
            phone=self.phone,
            apartment_number=self.apartment_number,
            rent_amount=self.rent_amount,
            rent_status=self.rent_status,
            due_date=self.due_date,
            amount_due=self.amount_due,
            last_payment_date=self.last_payment_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
            archived_by='System',
            archive_reason='Tenant deleted'
        )
        
        # Log the deletion
        TenantHistory.objects.create(
            tenant_name=self.name,
            apartment_number=self.apartment_number,
            action='deleted',
            description=f'Tenant {self.name} was deleted from apartment {self.apartment_number}',
            changed_by='System'
        )
        
        super().delete(*args, **kwargs)


class Payment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES, default='Full')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Paid')
    notes = models.TextField(blank=True, help_text="Optional notes about this payment")
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.tenant.name} - KSh {self.amount} - {self.status}"
    
    def delete(self, *args, **kwargs):
        """Override delete to archive payment before deletion"""
        # Archive payment before deletion
        ArchivedPayment.objects.create(
            original_id=self.id,
            tenant_name=self.tenant.name,
            tenant_apartment=self.tenant.apartment_number,
            amount=self.amount,
            date=self.date.date(),
            status=self.status,
            payment_type=self.payment_type,
            notes=self.notes,
            created_at=self.date,
            archived_by='System',
            archive_reason='Payment deleted'
        )
        
        # Log the deletion
        PaymentHistory.objects.create(
            tenant_name=self.tenant.name,
            apartment_number=self.tenant.apartment_number,
            payment_amount=self.amount,
            action='deleted',
            description=f'Payment of KSh {self.amount} was deleted for {self.tenant.name}',
            changed_by='System'
        )
        
        super().delete(*args, **kwargs)


class SMSLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='sms_logs')
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    response_data = models.JSONField(null=True, blank=True, help_text="API response data")
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.status} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"


class ArchivedTenant(models.Model):
    """Archive model for deleted tenants"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_id = models.UUIDField(help_text="Original tenant ID before deletion")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    apartment_number = models.CharField(max_length=20)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rent_status = models.CharField(max_length=20, choices=RENT_STATUS_CHOICES, default='Unpaid')
    due_date = models.IntegerField(default=1, help_text="Day of month when rent is due")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.CharField(max_length=100, default='System')
    archive_reason = models.CharField(max_length=200, default='Tenant deleted')
    
    class Meta:
        ordering = ['-archived_at']
        verbose_name = "Archived Tenant"
        verbose_name_plural = "Archived Tenants"
    
    def __str__(self):
        return f"Archived: {self.name} - {self.apartment_number}"


class ArchivedPayment(models.Model):
    """Archive model for deleted payments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_id = models.UUIDField(help_text="Original payment ID before deletion")
    tenant_name = models.CharField(max_length=100, help_text="Tenant name at time of deletion")
    tenant_apartment = models.CharField(max_length=20, help_text="Apartment number at time of deletion")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Paid')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='Full')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.CharField(max_length=100, default='System')
    archive_reason = models.CharField(max_length=200, default='Payment deleted')
    
    class Meta:
        ordering = ['-archived_at']
        verbose_name = "Archived Payment"
        verbose_name_plural = "Archived Payments"
    
    def __str__(self):
        return f"Archived: {self.tenant_name} - KSh {self.amount} - {self.status}"


class TenantHistory(models.Model):
    """History log for tenant changes"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('rent_paid', 'Rent Paid'),
        ('rent_unpaid', 'Rent Unpaid'),
        ('status_changed', 'Status Changed'),
        ('amount_changed', 'Amount Changed'),
        ('due_date_changed', 'Due Date Changed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_by = models.CharField(max_length=100, default='System')
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = "Tenant History"
        verbose_name_plural = "Tenant Histories"
    
    def __str__(self):
        return f"{self.tenant_name} - {self.action} - {self.changed_at.strftime('%Y-%m-%d %H:%M')}"


class PaymentHistory(models.Model):
    """History log for payment changes"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
        ('status_changed', 'Status Changed'),
        ('amount_changed', 'Amount Changed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=20)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_by = models.CharField(max_length=100, default='System')
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = "Payment History"
        verbose_name_plural = "Payment Histories"
    
    def __str__(self):
        return f"{self.tenant_name} - {self.action} - KSh {self.payment_amount}"
