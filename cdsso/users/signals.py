import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from cdsso.contrib.register.models import StudentRegistration

from .utils import update_user_on_codedevils_website

User = get_user_model()
logger = logging.getLogger()


def start_registration_workflow(instance: User):
    """
    Starts the registration workflow by creating a corresponding StudentRegistration entry for this user. Creating
    the model will automatically start the workflow for when the StudentRegistration saves.
    """
    StudentRegistration.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def update_codedevils_org(instance: User, created: bool, update_fields: frozenset, **kwargs):
    """Updates the CodeDevils website with new user information."""
    DEFAULT_FIELDS = settings.CODEDEVILS_WEBSITE_UPDATE_FIELDS
    FIELDS_TO_SKIP = settings.CODEDEVILS_WEBSITE_SKIP_FIELDS

    # update only if this is an active user
    if instance.is_active and not created:
        # username is required as a key to the graphql mutation
        user_data = {"username": instance.username}

        # update the default fields if no update_fields are specified
        fields_to_update = DEFAULT_FIELDS if not update_fields else update_fields

        # add each of the updated fields to the query
        for key in fields_to_update:
            # update the field if it's not a field to skip
            if key not in user_data and key not in FIELDS_TO_SKIP and getattr(instance, key, None):
                user_data.update({key: getattr(instance, key)})
        # send request with only updated fields
        try:
            ok, mutation_ok, data = update_user_on_codedevils_website(user_data=user_data)

            if not ok or not mutation_ok:
                error = data[0]["message"]
                logger.error(f"There was an issue updating user {instance.username}: {str(error)}")

        except Exception as e:
            logger.error(f"Failed to update user {instance.username}: {str(e)}")
