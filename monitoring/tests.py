from django.test import TestCase, Client
from django.urls import reverse
from .models import Service


class ServiceModelTest(TestCase):
    """Test the Service model"""

    def setUp(self):
        self.service = Service.objects.create(
            name="Payment Service",
            description="Handles payments",
            endpoint="https://api.example.com/pay",
            status="HEALTHY",
            response_time_ms=120.5,
            uptime_percentage=99.9,
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Payment Service")
        self.assertEqual(self.service.status, "HEALTHY")
        self.assertEqual(self.service.response_time_ms, 120.5)
        self.assertEqual(self.service.uptime_percentage, 99.9)

    def test_str_method(self):
        self.assertEqual(str(self.service), "Payment Service")

    def test_default_values(self):
        service = Service.objects.create(name="Test Service")
        self.assertEqual(service.status, "HEALTHY")
        self.assertEqual(service.response_time_ms, 0)
        self.assertEqual(service.uptime_percentage, 100)
        self.assertEqual(service.description, "")
        self.assertEqual(service.endpoint, "")