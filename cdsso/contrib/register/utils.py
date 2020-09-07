import requests
from django.conf import settings
from django.core.mail import send_mail

from .types import JWT


def email_user_complete_registration(email: str) -> None:
    """Sends a welcome message to anyone who finished the application process."""
    send_mail(
        subject="Welcome to CodeDevils",
        message="You've successfully signed up with CodeDevils! Login to https://codedevils.org to find out how "
        "being a member benefits you!",
        from_email=getattr(
            settings, "DEFAULT_FROM_EMAIL", "CodeDevils <donotreply@codedevils.org>"
        ),
        recipient_list=[email],
    )


def get_flameboi_jwt() -> JWT:
    """
    TODO Need to validate how the format will be.
    Gets the access and refresh tokens from Flameboi.

    Returns:
        The access and refresh tokens as a tuple.
    """
    url = settings.FLAMEBOI_API_URL
    username = settings.FLAMEBOI_API_USERNAME
    password = settings.FLAMEBOI_API_PASSWORD

    response = requests.post(url=url, json={"username": username, "password": password})
    if response.status_code == 200:
        data = response.json()
        if "access" not in data or "refresh" not in data:
            raise KeyError("invalid format")
        return data["access"], data["refresh"]
    else:
        raise requests.HTTPError("invalid status code")
