from cas_server import views
from django.conf.urls import url, re_path
from django.urls import path
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
from django.views.generic import RedirectView

from .views import sso_login_view, sso_logout_view

app_name = "cas_server"

urlpatterns = [
    re_path(
        r"^$",
        RedirectView.as_view(pattern_name="cas_server:login", permanent=False, query_string=True)
    ),
    path("login/", sensitive_post_parameters("password")(sso_login_view), name="login"),
    path("logout/", sso_logout_view, name="logout"),
    re_path("^validate$", views.Validate.as_view(), name="validate"),
    re_path(
        "^serviceValidate$",
        views.ValidateService.as_view(allow_proxy_ticket=False),
        name="serviceValidate"
    ),
    re_path(
        "^proxyValidate$",
        views.ValidateService.as_view(allow_proxy_ticket=True),
        name="proxyValidate"
    ),
    re_path("^proxy$", views.Proxy.as_view(), name="proxy"),
    re_path(
        "^p3/serviceValidate$",
        views.ValidateService.as_view(allow_proxy_ticket=False),
        name="p3_serviceValidate"
    ),
    re_path(
        "^p3/proxyValidate$",
        views.ValidateService.as_view(allow_proxy_ticket=True),
        name="p3_proxyValidate"
    ),
    re_path("^samlValidate$", views.SamlValidate.as_view(), name="samlValidate"),
    re_path(
        "^auth$",
        sensitive_variables("password", "secret")(
            sensitive_post_parameters("password", "secret")(
                views.Auth.as_view()
            )
        ),
        name="auth"
    ),
    re_path("^federate(?:/(?P<provider>([^/]+)))?$", views.FederateAuth.as_view(), name="federateAuth"),
]
