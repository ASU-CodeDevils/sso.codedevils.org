from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import KnownMember, StudentRegistration
from .tasks import notify_sds_registration, register_on_slack
from .utils import email_user_complete_registration


@receiver(pre_save, sender=StudentRegistration)
def check_known_members(instance: StudentRegistration, **kwargs):
    """
    Checks the current known members for the current registering user. If the user is a known
    member, their information is updated after registration.

    Args:
        instance (StudentRegistration): The student registration instance.
    """
    try:
        known_member = KnownMember.objects.get(email__exact=instance.user.email)
        instance.slack_registered = known_member.slack_registered
        instance.sds_registered = known_member.sds_registered
        instance.user.name = known_member.name
        instance.user.save()
        known_member.delete()  # delete the known member to save space in the database
    except KnownMember.DoesNotExist:
        pass


@receiver(post_save, sender=StudentRegistration)
def notify_complete_registration(instance: StudentRegistration, **kwargs):
    """
    Notifies the user when their registration has been updated.

    Args:
        instance (StudentRegistration): The student registration instance.
    """

    if settings.RUN_REGISTRATION_POST_SAVE_SIGNAL:

        # add users to slack automatically with Flameboi util
        if (
            settings.REGISTER_SLACK_USERS_WITH_FLAMEBOI
            and not instance.slack_registered
        ):
            register_on_slack.delay(emails=[instance.user.email])

        # notify managers of new users to be added to SunDevilSync
        if (
            settings.NOTIFY_MANAGERS_SDS_REGISTRATION
            and not instance.sds_registered
            and not instance._sds_notified
        ):
            notify_sds_registration.delay(instance.user.email)
            instance._sds_notified = True

        # notify a user if their registration has been completed
        if (
            settings.SEND_COMPLETED_REGISTRATION_NOTIFICATION
            and instance.completed_registration
        ):
            # TODO send the user an email saying their registration has been completed
            email_user_complete_registration(email=instance.user.email)
