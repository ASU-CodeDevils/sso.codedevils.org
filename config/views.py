from cas_server.views import LoginView, LogoutView
from django.contrib import auth


class SSOLoginView(LoginView):
    """This login view is overriden so the user can be logged into both the CAS server and this site."""

    def post(self, request, *args, **kwargs):
        # process the CAS login first
        response = super().post(request, *args, **kwargs)

        # then login the user to this site
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request=request, user=user)
        return response


sso_login_view = SSOLoginView.as_view()


class SSOLogoutView(LogoutView):
    """This logout view is overriden so the user can be logged out of session on both CAS and this site."""

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auth.logout(request=request)
        return response


sso_logout_view = SSOLogoutView.as_view()
