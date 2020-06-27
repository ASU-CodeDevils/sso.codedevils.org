from django.conf import settings
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter

from cdsso.users.api.views import UserViewSet
from config.drf import schema_view

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"

# DRF YASG
urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc")
]

urlpatterns += router.urls
