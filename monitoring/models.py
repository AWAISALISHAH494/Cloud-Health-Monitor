from django.db import models


class Service(models.Model):

    STATUS_CHOICES = [
        ("HEALTHY", "Healthy"),
        ("DEGRADED", "Degraded"),
        ("DOWN", "Down"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    endpoint = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="HEALTHY",
    )

    response_time_ms = models.FloatField(default=0)
    uptime_percentage = models.FloatField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name