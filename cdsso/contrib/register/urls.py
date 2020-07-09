from django.urls import path

from .views import registration_status_view, student_registration_view

app_name = "register"
urlpatterns = [
    path("", student_registration_view, name="index"),
    path("status/", registration_status_view, name="status")
]
