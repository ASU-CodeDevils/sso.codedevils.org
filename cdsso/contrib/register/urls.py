from django.urls import path

from .views import (
    registration_detail_view,
    registration_list_view,
    registration_status_view,
    student_registration_redirect_view,
)

app_name = "register"
urlpatterns = [
    path("", student_registration_redirect_view, name="index"),
    path("status/", registration_status_view, name="status"),
    path("registrations/", registration_list_view, name="registrations"),
    path(
        "registrations/<int:pk>/", registration_detail_view, name="registration-detail"
    ),
]
