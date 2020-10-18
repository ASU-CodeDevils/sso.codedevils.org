import logging
import re

from django.shortcuts import redirect

from .models import StudentRegistration

# urls that will not be redirected to the status page if the user is not registered
# TODO make this regex to account for end slashes
SAFE_URLS = (
    "/accounts/signup", "/accounts/signup/",
    "/accounts/logout", "/accounts/logout/",
    "/join/status/", "/join/status/",
    "/cas/logout", "/cas/logout/"
)


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
        reg_path_regex = re.compile(".+\.\w+", re.IGNORECASE)  # noqa W605

        whitelisted_path = request.path.endswith(SAFE_URLS)
        if (
            request.user.is_authenticated
            and not reg_path_regex.match(request.path)
            and request.path not in SAFE_URLS
            and not whitelisted_path
        ):
            reg_info, _ = StudentRegistration.objects.get_or_create(user=request.user)

            # redirect to registration page only if the user is missing a step in the registration
            # process
            if not reg_info.completed_registration():
                self.logger.info(
                    "User {} [{}] has not completed the registration process. Redirecting...".format(
                        request.user.username, request.user.id
                    )
                )
                return redirect("register:status")
        return response
