from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, RedirectView, TemplateView

from .models import StudentRegistration

User = get_user_model()


class RegistrationStatusView(LoginRequiredMixin, TemplateView):
    template_name = "register/status.html"


registration_status_view = RegistrationStatusView.as_view()


class UserRegistrationRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "account_signup"


student_registration_redirect_view = UserRegistrationRedirectView.as_view()


class RegistrationViewAbstract(LoginRequiredMixin):
    """Requires admins for registration detail and list views."""

    login_url = "admin:login"
    permission_denied_message = (
        "You must be a website administrator to access this page"
    )

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class RegistrationListView(RegistrationViewAbstract, ListView):
    model = StudentRegistration
    context_object_name = "student_registrations"
    paginate_by = settings.REGISTRATION_PAGINATION
    template_name = "register/registration_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slack_emails = StudentRegistration.todo_registrations.filter(
            slack_registered=False
        )
        if slack_emails:
            context["slack_student_emails"] = ",".join(
                list(
                    slack_emails.filter(user__is_alumni=False).values_list(
                        "user__email", flat=True
                    )
                )
            )
            context["slack_alumni_emails"] = ",".join(
                list(
                    slack_emails.filter(user__is_alumni=True).values_list(
                        "user__email", flat=True
                    )
                )
            )
        sds_emails = StudentRegistration.todo_registrations.filter(sds_registered=False)
        if sds_emails:
            context["sds_student_emails"] = "\n".join(
                list(
                    sds_emails.filter(user__is_alumni=False).values_list(
                        "user__email", flat=True
                    )
                )
            )
            context["sds_alumni_emails"] = "\n".join(
                list(
                    sds_emails.filter(user__is_alumni=True).values_list(
                        "user__email", flat=True
                    )
                )
            )
        return context


registration_list_view = RegistrationListView.as_view()


class RegistrationDetailView(RegistrationViewAbstract, DetailView):
    model = User
    context_object_name = "user"
    template_name = "register/registration_detail.html"

    def get_context_data(self, **kwargs):
        """
        Overrides this method to add the user's registration.
        """
        context = super().get_context_data(**kwargs)
        context["registration"] = StudentRegistration.objects.get(user=context["user"])
        return context

    def get(self, request, *args, **kwargs):
        """
        Overrides the get request to account for parameters. The parameters ``slack`` and
        ``sds`` can be set to *true* or *false* to update the student's registration.

        Args:
            request (HttpResponse): The request object.
        """
        self.object = self.get_object()  # required for overriding the get request
        context = self.get_context_data(**kwargs)
        registration = context["registration"]
        # accept sds and slack arguments if they're passed and update the user
        # registration accordingly
        if "slack" in request.GET:
            slack_param = request.GET.get("slack")
            if slack_param == "true":
                registration.slack_registered = True
            if slack_param == "false":
                registration.slack_registered = False
            registration.save()
        if "sds" in request.GET:
            sds_param = request.GET.get("sds")
            if sds_param == "true":
                registration.sds_registered = True
            if sds_param == "false":
                registration.sds_registered = False
            registration.save()
        return self.render_to_response(context=context)


registration_detail_view = RegistrationDetailView.as_view()
