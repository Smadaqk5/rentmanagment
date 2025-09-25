from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/add/', views.add_tenant, name='add_tenant'),
    path('tenants/<uuid:tenant_id>/edit/', views.edit_tenant, name='edit_tenant'),
    path('tenants/<uuid:tenant_id>/delete/', views.delete_tenant, name='delete_tenant'),
    path('tenants/<uuid:tenant_id>/mark-paid/', views.mark_rent_paid, name='mark_rent_paid'),
    path('tenants/<uuid:tenant_id>/send-reminder/', views.send_reminder, name='send_reminder'),
    path('tenants/<uuid:tenant_id>/partial-payment/', views.add_partial_payment, name='add_partial_payment'),
    path('payments/', views.payment_history, name='payment_history'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/<uuid:payment_id>/delete/', views.delete_payment, name='delete_payment'),
    path('analytics/', views.analytics, name='analytics'),
    path('records/', views.record_management, name='record_management'),
    path('records/bulk-delete-tenants/', views.bulk_delete_tenants, name='bulk_delete_tenants'),
    path('records/bulk-delete-payments/', views.bulk_delete_payments, name='bulk_delete_payments'),
    path('records/clear-old-payments/', views.clear_old_payments, name='clear_old_payments'),
    path('records/export/', views.export_data, name='export_data'),
    path('sms/', views.sms_logs, name='sms_logs'),
    path('sms/send-custom/<uuid:tenant_id>/', views.send_custom_sms, name='send_custom_sms'),
    path('sms/bulk-reminder/', views.bulk_sms_reminder, name='bulk_sms_reminder'),
]
