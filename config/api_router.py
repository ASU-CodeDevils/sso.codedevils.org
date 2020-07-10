from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.views import APIView

from cdsso.contrib.countries.api.views import CountryViewSet
from cdsso.contrib.register.api.views import StudentRegistrationViewSet
from cdsso.users.api.views import UserViewSet
from config.drf import schema_view

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("countries", CountryViewSet)
router.register("registration", StudentRegistrationViewSet)
router.register("users", UserViewSet)


# test API view
class TestView(APIView):
    """Test API endpoint view."""
    authentication_classes = [authentication.TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "test"}, content_type="application/json")


app_name = "api"

# DRF YASG
urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # test endpoint
    path("test/", TestView.as_view(), name="test")
]

urlpatterns += router.urls
