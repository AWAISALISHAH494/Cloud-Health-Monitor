from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "status",
        "response_time_ms",
        "uptime_percentage",
        "updated_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "name",
        "description",
    )