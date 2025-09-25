from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Tenant, Payment


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone', 'apartment_number', 'rent_amount', 'due_date', 'rent_status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254712345678'}),
            'apartment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount in KSh'}),
            'due_date': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '31', 'placeholder': 'Day of month (1-31)'}),
            'rent_status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('apartment_number', css_class='form-group col-md-6 mb-0'),
                Column('rent_amount', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('due_date', css_class='form-group col-md-6 mb-0'),
                Column('rent_status', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Tenant', css_class='btn btn-primary')
        )


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['tenant', 'amount', 'payment_type', 'status', 'notes']
        widgets = {
            'tenant': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount in KSh'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes about this payment'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'tenant',
            Row(
                Column('amount', css_class='form-group col-md-6 mb-0'),
                Column('payment_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'status',
            'notes',
            Submit('submit', 'Record Payment', css_class='btn btn-success')
        )
