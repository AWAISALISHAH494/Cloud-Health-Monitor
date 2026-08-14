from django.shortcuts import render, redirect, get_object_or_404

from .models import Service


def dashboard(request):

    services = Service.objects.all()

    total_services = services.count()
    healthy_services = services.filter(status="HEALTHY").count()
    degraded_services = services.filter(status="DEGRADED").count()
    down_services = services.filter(status="DOWN").count()

    context = {
        "services": services,
        "total_services": total_services,
        "healthy_services": healthy_services,
        "degraded_services": degraded_services,
        "down_services": down_services,
    }

    return render(
        request,
        "monitoring/dashboard.html",
        context,
    )


def service_create(request):

    if request.method == "POST":

        Service.objects.create(
            name=request.POST["name"],
            description=request.POST.get("description", ""),
            endpoint=request.POST.get("endpoint", ""),
            status=request.POST["status"],
            response_time_ms=request.POST.get(
                "response_time_ms", 0
            ),
            uptime_percentage=request.POST.get(
                "uptime_percentage", 100
            ),
        )

        return redirect("dashboard")

    return render(
        request,
        "monitoring/service_form.html",
    )


def service_edit(request, service_id):

    service = get_object_or_404(
        Service,
        id=service_id,
    )

    if request.method == "POST":

        service.name = request.POST["name"]
        service.description = request.POST.get(
            "description",
            "",
        )
        service.endpoint = request.POST.get(
            "endpoint",
            "",
        )
        service.status = request.POST["status"]

        service.response_time_ms = request.POST.get(
            "response_time_ms",
            0,
        )

        service.uptime_percentage = request.POST.get(
            "uptime_percentage",
            100,
        )

        service.save()

        return redirect("dashboard")

    return render(
        request,
        "monitoring/service_form.html",
        {"service": service},
    )


def service_delete(request, service_id):

    service = get_object_or_404(
        Service,
        id=service_id,
    )

    if request.method == "POST":
        service.delete()
        return redirect("dashboard")

    return render(
        request,
        "monitoring/service_confirm_delete.html",
        {"service": service},
    )