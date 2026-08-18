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


class DashboardViewTest(TestCase):
    """Test the dashboard view"""

    def setUp(self):
        self.client = Client()
        Service.objects.create(name="Service A", status="HEALTHY")
        Service.objects.create(name="Service B", status="DEGRADED")
        Service.objects.create(name="Service C", status="DOWN")
        Service.objects.create(name="Service D", status="HEALTHY")

    def test_dashboard_status_code(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        response = self.client.get(reverse("dashboard"))
        self.assertTemplateUsed(response, "monitoring/dashboard.html")

    def test_dashboard_stats(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.context["total_services"], 4)
        self.assertEqual(response.context["healthy_services"], 2)
        self.assertEqual(response.context["degraded_services"], 1)
        self.assertEqual(response.context["down_services"], 1)

    def test_dashboard_contains_services(self):
        response = self.client.get(reverse("dashboard"))
        self.assertContains(response, "Service A")
        self.assertContains(response, "Service B")
        self.assertContains(response, "Service C")

class ServiceCreateViewTest(TestCase):
    """Test Add Service view"""

    def setUp(self):
        self.client = Client()
        self.url = reverse("service_create")

    def test_create_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "monitoring/service_form.html")

    def test_create_service_success(self):
        data = {
            "name": "New API",
            "description": "Test API",
            "endpoint": "https://api.test.com",
            "status": "HEALTHY",
            "response_time_ms": 85,
            "uptime_percentage": 99.5,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(Service.objects.count(), 1)

        service = Service.objects.first()
        self.assertEqual(service.name, "New API")
        self.assertEqual(service.status, "HEALTHY")
        self.assertEqual(service.response_time_ms, 85)

    def test_create_service_minimal(self):
        data = {
            "name": "Minimal Service",
            "status": "DOWN",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Service.objects.count(), 1)

class ServiceEditViewTest(TestCase):
    """Test Edit Service view"""

    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name="Old Name",
            status="HEALTHY",
            response_time_ms=100,
            uptime_percentage=98,
        )
        self.url = reverse("service_edit", args=[self.service.id])

    def test_edit_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "monitoring/service_form.html")
        self.assertContains(response, "Old Name")

    def test_edit_service_success(self):
        data = {
            "name": "Updated Name",
            "description": "Updated description",
            "endpoint": "https://new.endpoint.com",
            "status": "DEGRADED",
            "response_time_ms": 250,
            "uptime_percentage": 95.5,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        self.service.refresh_from_db()
        self.assertEqual(self.service.name, "Updated Name")
        self.assertEqual(self.service.status, "DEGRADED")
        self.assertEqual(self.service.response_time_ms, 250)
        self.assertEqual(self.service.uptime_percentage, 95.5)

    def test_edit_nonexistent_service(self):
        url = reverse("service_edit", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)