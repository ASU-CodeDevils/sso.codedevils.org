from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class CompletedRegistrationManager(models.Manager):
    """Manager to extract all students that have completed registration."""
    def get_queryset(self):
        queryset = super(CompletedRegistrationManager, self).get_queryset()
        queryset = queryset.filter(slack_registered=True, sds_registered=True)
        return queryset


class NotCompletedRegistrationManager(models.Manager):
    """Manager to extract all students that have not completed registration."""
    def get_queryset(self):
        queryset = super(NotCompletedRegistrationManager, self).get_queryset()
        queryset = queryset.filter(Q(slack_registered=False) | Q(sds_registered=False))
        return queryset


class StudentRegistration(models.Model):
    """Defines the steps required for registering a student."""
    user = models.OneToOneField(User, db_column="UserId", on_delete=models.CASCADE, blank=False,
                                verbose_name=_("User"),
                                help_text=_("This user's progress in the registration process."))

    # individual steps required to fully register
    slack_registered = models.BooleanField(db_column="SlackRegistered", null=False, default=False,
                                           verbose_name=_("Registered on Slack"),
                                           help_text=_("The user has been registered on Slack"))
    sds_registered = models.BooleanField(db_column="SDSRegistered", null=False, default=False,
                                         verbose_name=_("Registered on SunDevilSync"),
                                         help_text=_("The user has been registered on SunDevilSync. This is True by "
                                                     "default for alumni."))

    # custom managers
    objects = models.Manager()
    completed_registrations = CompletedRegistrationManager()
    todo_registrations = NotCompletedRegistrationManager()

    class Meta:
        verbose_name = _("Student Registration")
        verbose_name_plural = _("Student Registration")

    def __str__(self):
        return f"{self.user.name} [done: {self.completed_registration()}]"

    def completed_registration(self):
        return self.slack_registered and self.sds_registered

    def save(self, *args, **kwargs):
        """Sets SDS registration to True if the user is registering as alumni."""
        if self.user.is_alumni:
            self.sds_registered = True
        super().save(*args, **kwargs)
