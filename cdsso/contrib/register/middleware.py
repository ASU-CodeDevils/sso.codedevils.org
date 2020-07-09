import re
import logging

from django.shortcuts import redirect

from .models import StudentRegistration


class UserRegistrationConfirmationMiddleware:
    """
    Middleware used to confirm that the logged-in user has completed the registration process. If not, the user is
    redirected to the status page, which details the status of their registration.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger()

    def __call__(self, request):
        response = self.get_response(request)

        # this will stop any static pages (i.e. css or js files) from being redirected
        reg_path_regex = re.compile('.+\.\w+', re.IGNORECASE)  # noqa W605

        # only run through middleware if the user is authenticated, is not already going to the
        # student registration page, and a file is not being loaded
        print(request.path)
        signup_path = request.path.endswith("/accounts/signup/") or request.path.endswith("/join/status/")
        logout_path = request.path.endswith("/cas/lougout") or request.path.endswith("/accounts/logout/")
        print(signup_path)
        if request.user.is_authenticated and not reg_path_regex.match(request.path) \
                and not signup_path and not logout_path:
            reg_info, _ = StudentRegistration.objects.get_or_create(user=request.user)

            # redirect to registration page only if the user is missing a step in the registration
            # process
            if not reg_info.completed_registration():
                self.logger.info("User {} [{}] has not completed the registration process. Redirecting...".format(
                    request.user.username, request.user.id
                ))
                return redirect("register:status")
        return response
