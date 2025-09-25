from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Tenant, Payment


class AnalyticsService:
    @staticmethod
    def get_monthly_income(year=None, month=None):
        """Get monthly income for a specific month"""
        if not year:
            year = timezone.now().year
        if not month:
            month = timezone.now().month
        
        start_date = timezone.datetime(year, month, 1)
        if month == 12:
            end_date = timezone.datetime(year + 1, 1, 1)
        else:
            end_date = timezone.datetime(year, month + 1, 1)
        
        payments = Payment.objects.filter(
            date__gte=start_date,
            date__lt=end_date,
            status='Paid'
        )
        
        total_income = payments.aggregate(total=Sum('amount'))['total'] or 0
        payment_count = payments.count()
        
        return {
            'total_income': total_income,
            'payment_count': payment_count,
            'month': month,
            'year': year,
            'month_name': start_date.strftime('%B')
        }
    
    @staticmethod
    def get_yearly_income(year=None):
        """Get yearly income breakdown by month"""
        if not year:
            year = timezone.now().year
        
        monthly_data = []
        for month in range(1, 13):
            month_data = AnalyticsService.get_monthly_income(year, month)
            monthly_data.append(month_data)
        
        total_yearly = sum(month['total_income'] for month in monthly_data)
        
        return {
            'year': year,
            'monthly_data': monthly_data,
            'total_yearly': total_yearly
        }
    
    @staticmethod
    def get_tenant_analytics():
        """Get tenant payment analytics"""
        total_tenants = Tenant.objects.count()
        paid_tenants = Tenant.objects.filter(rent_status='Paid').count()
        unpaid_tenants = Tenant.objects.filter(rent_status='Unpaid').count()
        partial_tenants = Tenant.objects.filter(rent_status='Partial').count()
        overdue_tenants = Tenant.objects.filter(rent_status='Overdue').count()
        
        total_rent_due = Tenant.objects.aggregate(
            total=Sum('rent_amount')
        )['total'] or 0
        
        total_amount_due = Tenant.objects.aggregate(
            total=Sum('amount_due')
        )['total'] or 0
        
        collection_rate = (paid_tenants / total_tenants * 100) if total_tenants > 0 else 0
        
        return {
            'total_tenants': total_tenants,
            'paid_tenants': paid_tenants,
            'unpaid_tenants': unpaid_tenants,
            'partial_tenants': partial_tenants,
            'overdue_tenants': overdue_tenants,
            'total_rent_due': total_rent_due,
            'total_amount_due': total_amount_due,
            'collection_rate': collection_rate
        }
    
    @staticmethod
    def get_payment_trends(days=30):
        """Get payment trends for the last N days"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        payments = Payment.objects.filter(
            date__gte=start_date,
            date__lte=end_date,
            status='Paid'
        ).order_by('date')
        
        daily_income = {}
        for payment in payments:
            date_str = payment.date.date().strftime('%Y-%m-%d')
            if date_str not in daily_income:
                daily_income[date_str] = 0
            daily_income[date_str] += float(payment.amount)
        
        return {
            'daily_income': daily_income,
            'total_period_income': sum(daily_income.values()),
            'days': days
        }
    
    @staticmethod
    def get_overdue_tenants():
        """Get list of overdue tenants"""
        overdue_tenants = []
        for tenant in Tenant.objects.filter(rent_status='Overdue'):
            next_due = tenant.get_next_due_date()
            days_overdue = (timezone.now().date() - next_due.date()).days
            overdue_tenants.append({
                'tenant': tenant,
                'days_overdue': days_overdue,
                'amount_due': tenant.amount_due
            })
        
        return sorted(overdue_tenants, key=lambda x: x['days_overdue'], reverse=True)
