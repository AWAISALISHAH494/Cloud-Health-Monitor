from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "services/add/",
        views.service_create,
        name="service_create",
    ),

    path(
        "services/<int:service_id>/edit/",
        views.service_edit,
        name="service_edit",
    ),

    path(
        "services/<int:service_id>/delete/",
        views.service_delete,
        name="service_delete",
    ),
]