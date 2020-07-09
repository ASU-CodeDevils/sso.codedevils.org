from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView


class RegistrationStatusView(LoginRequiredMixin, TemplateView):
    template_name = "register/status.html"


registration_status_view = RegistrationStatusView.as_view()


class UserRegistrationRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "account_signup"


student_registration_redirect_view = UserRegistrationRedirectView.as_view()
