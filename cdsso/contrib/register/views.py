from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView

from .forms import StudentRegistrationForm


class RegistrationStatusView(LoginRequiredMixin, TemplateView):
    template_name = "register/status.html"


registration_status_view = RegistrationStatusView.as_view()


class UserRegistrationFormView(FormView):
    template_name = "register/student_registration.html"
    form_class = StudentRegistrationForm
    success_url = "/join/status/"

    def form_valid(self, form):
        return super().form_valid(form)


student_registration_view = UserRegistrationFormView.as_view()
