import logging
from typing import List

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers
from django.core.validators import validate_email

from config import celery_app

from .models import StudentRegistration
from .types import SlackUserObject
from .utils import get_flameboi_jwt

logger = logging.getLogger()
Emails = List[str]
User = get_user_model()


@celery_app.task()
def register_on_slack(emails: Emails):
    """
    Since Flameboi cannot (as of the initial version of Flameboi and v1.0.1 of SSO) register members on Slack,
    this simply checks Slack to see if the user has been registered yet or not. If the user is registered on
    Slack, their information is automatically populated.

    Args:
        email (Emails): The list of emails to be checked.
    """
    if settings.FLAMEBOI["REGISTER_SLACK_USERS_WITH_FLAMEBOI"]:
        # validate emails, this will raise a ValidationError
        invalid_emails = []
        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                logger.warning(f"Invalid email to add to Slack: {email}")
                invalid_emails.append(email)

        # remove invalid emails
        valid_emails = [email for email in emails if email not in invalid_emails]

        # TODO check this endpoint
        url = settings.FLAMEBOI["API_URL"] + "get_student/"

        # get the access token needed for the requests
        try:
            access, _ = get_flameboi_jwt()
        except (KeyError, requests.HTTPError):
            logger.error("Failed to authenticate against Flameboi with JWT")

        # for the valid emails, check against Slack for membership
        for email in valid_emails:
            response = requests.get(
                url=url,
                headers={"Authorization": "Bearer " + access, "Accept": "application/json"}
            )
            if response.status_code == 200:
                data: SlackUserObject = response.json()
                if data["ok"]:
                    member = User.objects.get(email__exact=email)
                    user = data["user"]
                    profile = user["profile"]
                    # update the user
                    member.slack_id = user["id"]
                    member.tz_offset = user["tz_offset"]
                    member.name = profile["real_name"]
                    member.first_name = user["profile"]
                    member.image_24 = user["profile"]["image_24"]
                    member.image_512 = user["profile"]["image_512"]
                    member.save()
                    # update registration
                    member.studentregistration.slack_registered = True
                    member.studentregistration.save()
                    logger.info("New member registered on Slack: {}".format(email))
                # will error if the user has not been found
                else:
                    error = data["error"]
                    if error == "user_not_found":
                        logger.warning("User registered on SSO, but not on Slack: {}".format(email))
                    else:
                        logger.error("An unknown error occurred with the Flameboi API: {}".format(error))
            else:
                logger.error("Invalid status code {} when retrieving member info {}".format(
                    response.status_code, email
                ))
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
