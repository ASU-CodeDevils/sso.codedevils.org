from django.conf import settings
from django.core.mail import send_mail


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
