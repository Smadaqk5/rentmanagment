from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Tenant, Payment


class TenantModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="John Doe",
            phone="+254712345678",
            apartment_number="A101",
            rent_amount=500.00,
            rent_status="Unpaid"
        )

    def test_tenant_creation(self):
        self.assertEqual(self.tenant.name, "John Doe")
        self.assertEqual(self.tenant.phone, "+254712345678")
        self.assertEqual(self.tenant.apartment_number, "A101")
        self.assertEqual(self.tenant.rent_amount, 500.00)
        self.assertEqual(self.tenant.rent_status, "Unpaid")

    def test_tenant_string_representation(self):
        self.assertEqual(str(self.tenant), "John Doe - Apt A101")


class PaymentModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Jane Smith",
            phone="+254798765432",
            apartment_number="B202",
            rent_amount=750.00,
            rent_status="Unpaid"
        )
        self.payment = Payment.objects.create(
            tenant=self.tenant,
            amount=750.00,
            status="Paid"
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.tenant, self.tenant)
        self.assertEqual(self.payment.amount, 750.00)
        self.assertEqual(self.payment.status, "Paid")

    def test_payment_string_representation(self):
        self.assertEqual(str(self.payment), "Jane Smith - $750.00 - Paid")


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testlandlord',
            password='testpass123'
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_with_login(self):
        self.client.login(username='testlandlord', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
