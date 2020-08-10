import logging
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers
from django.core.validators import validate_email

from config import celery_app

from .models import StudentRegistration

logger = logging.getLogger()
Emails = List[str]


@celery_app.task()
def register_on_slack(emails: Emails):
    """
    Registers a single email or list of emails on Slack using Flameboi.
    """
    if settings.REGISTER_SLACK_USERS_WITH_FLAMEBOI:
        # validate emails, this will raise a ValidationError
        invalid_emails = []
        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                logger.warning(f"Invalid email to add to Slack: {email}")
                invalid_emails.append(email)

        # TODO implement Flameboi API
        pass
    else:
        logger.warning(
            "To add users to slack automatically, please set REGISTER_SLACK_USERS_WITH_FLAMEBOI to True"
        )


@celery_app.task()
def notify_sds_registration(email: str):
    """Notifies managers of this app to add a student to SunDevilSync."""
    if settings.NOTIFY_MANAGERS_SDS_REGISTRATION:
        SDS_URL = "https://asu.campuslabs.com/engage/actioncenter/organization/codedevils/roster/Roster/invite"
        mail_managers(
            subject="New CodeDevils Member",
            message="A new student has requested to join CodeDevils. Please add the following email to SunDevilSync:"
            "\n{}\n\nYou can add this student at: {}".format(email, SDS_URL),
        )
    else:
        logger.warning(
            "To notify managers of SDS registration, please set NOTIFY_MANAGERS_SDS_REGISTRATION to True"
        )


@celery_app.task()
def notify_managers_of_registrations():
    """Sends SSO managers an email of all users who have not completed their registration."""
    try:
        registrations = StudentRegistration.todo_registrations.all()
        registrations = registrations.values_list("user__email", flat=True)
        mail_managers(
            subject="Unfinished student registrations",
            message="The following users have not completed their registration:"
            + "\n* ".join(registrations),
        )
    except Exception as e:
        logger.error(
            "There was an issue emailing managers of missing registrations: " + str(e)
        )
