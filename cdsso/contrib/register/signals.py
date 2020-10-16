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
    known_member = KnownMember.objects.filter(email__exact=instance.user.email)
    if known_member:
        known_member = known_member.first()
        instance.slack_registered = known_member.slack_registered
        instance.sds_registered = known_member.sds_registered
        instance.user.name = known_member.name
        known_member.delete()  # delete the known member to save space in the database


@receiver(post_save, sender=StudentRegistration)
def notify_complete_registration(instance: StudentRegistration, **kwargs):
    """
    Notifies the user when their registration has been updated.

    Args:
        instance (StudentRegistration): The student registration instance.
    """

    if settings.RUN_REGISTRATION_POST_SAVE_SIGNAL:
        save_again = False  # needed for if we notify admin/the user

        # add users to slack automatically with Flameboi util
        if (
            settings.FLAMEBOI["REGISTER_SLACK_USERS_WITH_FLAMEBOI"]
            and not instance.slack_registered
            and not instance.slack_add_attempt
        ):
            register_on_slack.delay(emails=[instance.user.email])
            instance.slack_add_attempt = True
            save_again = True

        # notify managers of new users to be added to SunDevilSync
        if (
            settings.NOTIFY_MANAGERS_SDS_REGISTRATION
            and not instance.sds_registered
            and not instance.sds_notified
        ):
            notify_sds_registration.delay(instance.user.email)
            instance.sds_notified = True
            save_again = True

        # notify a user if their registration has been completed
        if (
            settings.SEND_COMPLETED_REGISTRATION_NOTIFICATION
            and instance.completed_registration
            and not instance.completed_registration_notification
            and not self._restart_registration
        ):
            # TODO send the user an email saying their registration has been completed
            email_user_complete_registration(email=instance.user.email)
            instance.completed_registration_notification = True
            save_again = True

        if save_again:
            instance.save()
