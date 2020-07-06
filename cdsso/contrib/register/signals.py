from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentRegistration
from .tasks import notify_sds_registration, register_on_slack


@receiver(post_save, sender=StudentRegistration)
def notify_complete_registration(sender, **kwargs):
    if settings.RUN_REGISTRATION_POST_SAVE_SIGNAL:

        # add users to slack automatically with Flameboi util
        if settings.REGISTER_SLACK_USERS_WITH_FLAMEBOI and not sender.user.slack_registered:
            register_on_slack.delay(emails=[sender.user.email])

        # notify managers of new users to be added to SunDevilSync
        if settings.NOTIFY_MANAGERS_SDS_REGISTRATION and not sender.user.sds_registered:
            notify_sds_registration.delay(sender.user.email)

        # notify a user if their registration has been completed
        if settings.SEND_COMPLETED_REGISTRATION_NOTIFICATION and sender.completed_registration():
            # TODO send the user an email saying their registration has been completed
            sender.user.email_user(
                subject="CodeDevils - Your Registration Has Completed!",
                message="Your registration is complete. Welcome to CodeDevils! Login to our website "
                        "to see everything CodeDevils has to offer! https://codedevils.org",
                from_email="CodeDevils <donotreply@codedevils.org>"
            )
