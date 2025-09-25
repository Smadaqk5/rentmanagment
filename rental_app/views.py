from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Tenant, Payment
from .forms import TenantForm, PaymentForm
from .africas_talking_service import AfricasTalkingService
from .analytics import AnalyticsService


@login_required
def dashboard(request):
    """Main dashboard view"""
    tenants = Tenant.objects.all()
    analytics = AnalyticsService.get_tenant_analytics()
    monthly_income = AnalyticsService.get_monthly_income()
    overdue_tenants = AnalyticsService.get_overdue_tenants()[:5]
    
    # Recent payments
    recent_payments = Payment.objects.select_related('tenant').order_by('-date')[:5]
    
    context = {
        'tenants': tenants,
        'recent_payments': recent_payments,
        'analytics': analytics,
        'monthly_income': monthly_income,
        'overdue_tenants': overdue_tenants,
    }
    return render(request, 'rental_app/dashboard.html', context)


@login_required
def tenant_list(request):
    """List all tenants"""
    tenants = Tenant.objects.all()
    return render(request, 'rental_app/tenant_list.html', {'tenants': tenants})


@login_required
def add_tenant(request):
    """Add a new tenant"""
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant added successfully!')
            return redirect('tenant_list')
    else:
        form = TenantForm()
    
    return render(request, 'rental_app/tenant_form.html', {'form': form, 'title': 'Add Tenant'})


@login_required
def edit_tenant(request, tenant_id):
    """Edit an existing tenant"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenant updated successfully!')
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant)
    
    return render(request, 'rental_app/tenant_form.html', {'form': form, 'title': 'Edit Tenant'})


@login_required
def delete_tenant(request, tenant_id):
    """Delete a tenant"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if request.method == 'POST':
        tenant.delete()
        messages.success(request, 'Tenant deleted successfully!')
        return redirect('tenant_list')
    
    return render(request, 'rental_app/confirm_delete.html', {'tenant': tenant})


@login_required
def mark_rent_paid(request, tenant_id):
    """Mark rent as paid and send confirmation"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if tenant.rent_status == 'Unpaid':
        tenant.rent_status = 'Paid'
        tenant.save()
        
        # Create payment record
        Payment.objects.create(
            tenant=tenant,
            amount=tenant.rent_amount,
            status='Paid'
        )
        
        # Send SMS confirmation
        sms = SMSMobileService()
        success, message = sms.send_rent_confirmation(tenant)
        
        if success:
            messages.success(request, f'Rent marked as paid and SMS confirmation sent to {tenant.name}!')
        else:
            messages.warning(request, f'Rent marked as paid but SMS failed: {message}')
    else:
        messages.info(request, 'Rent is already marked as paid.')
    
    return redirect('dashboard')


@login_required
def send_reminder(request, tenant_id):
    """Send SMS reminder to tenant"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    sms = SMSMobileService()
    success, message = sms.send_rent_reminder(tenant)
    
    if success:
        messages.success(request, f'SMS reminder sent to {tenant.name}!')
    else:
        messages.error(request, f'Failed to send SMS reminder: {message}')
    
    return redirect('dashboard')


@login_required
def payment_history(request):
    """View payment history"""
    payments = Payment.objects.select_related('tenant').order_by('-date')
    return render(request, 'rental_app/payment_history.html', {'payments': payments})


@login_required
def add_payment(request):
    """Add a manual payment record"""
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            # Update tenant amount due if payment is marked as paid
            if payment.status == 'Paid':
                payment.tenant.add_payment(payment.amount)
            messages.success(request, 'Payment recorded successfully!')
            return redirect('payment_history')
    else:
        form = PaymentForm()
    
    return render(request, 'rental_app/payment_form.html', {'form': form})


@login_required
def analytics(request):
    """Analytics dashboard"""
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    
    try:
        year = int(year)
        month = int(month)
    except (ValueError, TypeError):
        year = timezone.now().year
        month = timezone.now().month
    
    tenant_analytics = AnalyticsService.get_tenant_analytics()
    monthly_income = AnalyticsService.get_monthly_income(year, month)
    yearly_income = AnalyticsService.get_yearly_income(year)
    payment_trends = AnalyticsService.get_payment_trends(30)
    overdue_tenants = AnalyticsService.get_overdue_tenants()
    
    context = {
        'tenant_analytics': tenant_analytics,
        'monthly_income': monthly_income,
        'yearly_income': yearly_income,
        'payment_trends': payment_trends,
        'overdue_tenants': overdue_tenants,
        'current_year': year,
        'current_month': month,
    }
    return render(request, 'rental_app/analytics.html', context)


@login_required
def add_partial_payment(request, tenant_id):
    """Add a partial payment for a specific tenant"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        notes = request.POST.get('notes', '')
        
        try:
            amount = float(amount)
            if amount > 0:
                # Create payment record
                Payment.objects.create(
                    tenant=tenant,
                    amount=amount,
                    payment_type='Partial',
                    status='Paid',
                    notes=notes
                )
                
                # Update tenant amount due
                tenant.add_payment(amount)
                
                messages.success(request, f'Partial payment of KSh {amount} recorded for {tenant.name}!')
            else:
                messages.error(request, 'Payment amount must be greater than 0.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid payment amount.')
        
        return redirect('tenant_list')
    
    return render(request, 'rental_app/partial_payment_form.html', {'tenant': tenant})


@login_required
def record_management(request):
    """Record management dashboard"""
    # Get statistics
    total_tenants = Tenant.objects.count()
    total_payments = Payment.objects.count()
    
    # Get recent records
    recent_tenants = Tenant.objects.order_by('-created_at')[:10]
    recent_payments = Payment.objects.select_related('tenant').order_by('-date')[:10]
    
    # Get overdue tenants
    overdue_tenants = Tenant.objects.filter(rent_status='Overdue')[:5]
    
    context = {
        'total_tenants': total_tenants,
        'total_payments': total_payments,
        'recent_tenants': recent_tenants,
        'recent_payments': recent_payments,
        'overdue_tenants': overdue_tenants,
    }
    return render(request, 'rental_app/record_management.html', context)


@login_required
def bulk_delete_tenants(request):
    """Bulk delete tenants"""
    if request.method == 'POST':
        tenant_ids = request.POST.getlist('tenant_ids')
        if tenant_ids:
            deleted_count = 0
            for tenant_id in tenant_ids:
                try:
                    tenant = Tenant.objects.get(id=tenant_id)
                    tenant.delete()
                    deleted_count += 1
                except Tenant.DoesNotExist:
                    continue
            
            messages.success(request, f'Successfully deleted {deleted_count} tenants.')
        else:
            messages.warning(request, 'No tenants selected for deletion.')
        
        return redirect('record_management')
    
    # Get tenants for selection
    tenants = Tenant.objects.all()
    return render(request, 'rental_app/bulk_delete_tenants.html', {'tenants': tenants})


@login_required
def bulk_delete_payments(request):
    """Bulk delete payments"""
    if request.method == 'POST':
        payment_ids = request.POST.getlist('payment_ids')
        if payment_ids:
            deleted_count = 0
            for payment_id in payment_ids:
                try:
                    payment = Payment.objects.get(id=payment_id)
                    # Update tenant amount due before deleting payment
                    payment.tenant.amount_due += payment.amount
                    payment.tenant.update_status()
                    payment.delete()
                    deleted_count += 1
                except Payment.DoesNotExist:
                    continue
            
            messages.success(request, f'Successfully deleted {deleted_count} payments.')
        else:
            messages.warning(request, 'No payments selected for deletion.')
        
        return redirect('record_management')
    
    # Get payments for selection
    payments = Payment.objects.select_related('tenant').order_by('-date')
    return render(request, 'rental_app/bulk_delete_payments.html', {'payments': payments})


@login_required
def delete_payment(request, payment_id):
    """Delete a single payment"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        # Update tenant amount due before deleting payment
        payment.tenant.amount_due += payment.amount
        payment.tenant.update_status()
        payment.delete()
        
        messages.success(request, 'Payment deleted successfully!')
        return redirect('payment_history')
    
    return render(request, 'rental_app/confirm_delete_payment.html', {'payment': payment})


@login_required
def clear_old_payments(request):
    """Clear payments older than specified days"""
    if request.method == 'POST':
        days = int(request.POST.get('days', 365))
        cutoff_date = timezone.now() - timedelta(days=days)
        
        old_payments = Payment.objects.filter(date__lt=cutoff_date)
        count = old_payments.count()
        
        if count > 0:
            old_payments.delete()
            messages.success(request, f'Successfully deleted {count} payments older than {days} days.')
        else:
            messages.info(request, f'No payments found older than {days} days.')
        
        return redirect('record_management')
    
    return render(request, 'rental_app/clear_old_payments.html')


@login_required
def export_data(request):
    """Export data to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rental_data.csv"'
    
    writer = csv.writer(response)
    
    # Write tenants data
    writer.writerow(['TENANTS DATA'])
    writer.writerow(['Name', 'Phone', 'Apartment', 'Rent Amount', 'Amount Due', 'Status', 'Due Date', 'Created'])
    
    for tenant in Tenant.objects.all():
        writer.writerow([
            tenant.name,
            tenant.phone,
            tenant.apartment_number,
            tenant.rent_amount,
            tenant.amount_due,
            tenant.rent_status,
            tenant.due_date,
            tenant.created_at.strftime('%Y-%m-%d')
        ])
    
    writer.writerow([])  # Empty row
    
    # Write payments data
    writer.writerow(['PAYMENTS DATA'])
    writer.writerow(['Tenant', 'Amount', 'Type', 'Status', 'Date', 'Notes'])
    
    for payment in Payment.objects.select_related('tenant').all():
        writer.writerow([
            payment.tenant.name,
            payment.amount,
            payment.payment_type,
            payment.status,
            payment.date.strftime('%Y-%m-%d %H:%M'),
            payment.notes
        ])
    
    return response


@login_required
def sms_logs(request):
    """View SMS logs"""
    from .models import SMSLog
    
    tenant_id = request.GET.get('tenant_id')
    if tenant_id:
        tenant = get_object_or_404(Tenant, id=tenant_id)
        sms_logs = SMSLog.objects.filter(tenant=tenant).order_by('-sent_at')
    else:
        sms_logs = SMSLog.objects.select_related('tenant').order_by('-sent_at')
    
    # Get SMS statistics
    sms_service = AfricasTalkingService()
    stats = sms_service.get_sms_statistics()
    
    context = {
        'sms_logs': sms_logs,
        'stats': stats,
        'selected_tenant': tenant if tenant_id else None,
    }
    return render(request, 'rental_app/sms_logs.html', context)


@login_required
def send_custom_sms(request, tenant_id):
    """Send custom SMS to tenant"""
    tenant = get_object_or_404(Tenant, id=tenant_id)
    
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        
        if not message:
            messages.error(request, 'Please enter a message.')
            return redirect('send_custom_sms', tenant_id=tenant_id)
        
        sms = SMSMobileService()
        success, result_message = sms.send_custom_message(tenant, message)
        
        if success:
            messages.success(request, f'Custom SMS sent to {tenant.name}!')
        else:
            messages.error(request, f'Failed to send SMS: {result_message}')
        
        return redirect('tenant_list')
    
    return render(request, 'rental_app/send_custom_sms.html', {'tenant': tenant})


@login_required
def bulk_sms_reminder(request):
    """Send SMS reminders to multiple tenants"""
    if request.method == 'POST':
        tenant_ids = request.POST.getlist('tenant_ids')
        message_type = request.POST.get('message_type', 'rent_reminder')
        
        if not tenant_ids:
            messages.warning(request, 'No tenants selected.')
            return redirect('bulk_sms_reminder')
        
        sms = SMSMobileService()
        success_count = 0
        failure_count = 0
        
        for tenant_id in tenant_ids:
            try:
                tenant = Tenant.objects.get(id=tenant_id)
                
                if message_type == 'rent_reminder':
                    success, _ = sms.send_rent_reminder(tenant)
                elif message_type == 'payment_reminder':
                    success, _ = sms.send_payment_reminder(tenant, tenant.amount_due)
                else:
                    success = False
                
                if success:
                    success_count += 1
                else:
                    failure_count += 1
                    
            except Tenant.DoesNotExist:
                failure_count += 1
                continue
        
        messages.success(request, f'Bulk SMS completed: {success_count} sent, {failure_count} failed.')
        return redirect('record_management')
    
    # Get tenants for selection
    tenants = Tenant.objects.filter(rent_status__in=['Unpaid', 'Partial', 'Overdue'])
    return render(request, 'rental_app/bulk_sms_reminder.html', {'tenants': tenants})
