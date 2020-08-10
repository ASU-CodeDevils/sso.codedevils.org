from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentRegistration
from .tasks import notify_sds_registration, register_on_slack
from .utils import email_user_complete_registration


@receiver(post_save, sender=StudentRegistration)
def notify_complete_registration(instance: StudentRegistration, **kwargs):
    if settings.RUN_REGISTRATION_POST_SAVE_SIGNAL:

        # add users to slack automatically with Flameboi util
        if (
            settings.REGISTER_SLACK_USERS_WITH_FLAMEBOI
            and not instance.slack_registered
        ):
            register_on_slack.delay(emails=[instance.user.email])

        # notify managers of new users to be added to SunDevilSync
        if settings.NOTIFY_MANAGERS_SDS_REGISTRATION and not instance.sds_registered:
            notify_sds_registration.delay(instance.user.email)

        # notify a user if their registration has been completed
        if (
            settings.SEND_COMPLETED_REGISTRATION_NOTIFICATION
            and instance.completed_registration
        ):
            # TODO send the user an email saying their registration has been completed
            email_user_complete_registration(email=instance.user.email)
