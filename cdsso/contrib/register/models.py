from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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


class RegistrationModelAbstract(models.Model):
    # individual steps required to fully register
    slack_registered = models.BooleanField(
        db_column="SlackRegistered",
        null=False,
        default=False,
        verbose_name=_("Registered on Slack"),
        help_text=_("The user has been registered on Slack"),
    )
    sds_registered = models.BooleanField(
        db_column="SDSRegistered",
        null=False,
        default=False,
        verbose_name=_("Registered on SunDevilSync"),
        help_text=_(
            "The user has been registered on SunDevilSync. This is True by "
            "default for alumni."
        ),
    )

    class Meta:
        abstract = True


class StudentRegistration(RegistrationModelAbstract):
    """Defines the steps required for registering a student."""

    user = models.OneToOneField(
        User,
        db_column="UserId",
        on_delete=models.CASCADE,
        blank=False,
        verbose_name=_("User"),
        help_text=_("This user's progress in the registration process."),
    )
    date_registered = models.DateTimeField(
        db_column="DateRegistered",
        auto_now_add=True,
        verbose_name=_("Date Registered"),
        help_text=_("The date/time the student submitted their registration form"),
    )

    # these flags are used to manage notifications
    sds_notified = models.BooleanField(
        db_column="SdsNotified",
        default=False,
        null=False,
        verbose_name=_("SunDevilSync Notification"),
        help_text=_(
            "Flag to track whether a CodeDevils officer has been notified that this "
            "student needs to be added to SunDevilSync"
        ),
    )
    slack_add_attempt = models.BooleanField(
        db_column="SlackAddAttempt",
        default=False,
        null=False,
        verbose_name=_("Slack Add Attempt"),
        help_text=_(
            "Flag to track if the API was used previously to add this user to Slack. "
            "This stops consecutive attempts of adding this user."
        ),
    )
    completed_registration_notification = models.BooleanField(
        db_column="CompletedRegistrationNotification",
        default=False,
        null=False,
        verbose_name=_("Completed Registration Notification"),
        help_text=_(
            "Flag to track if this user has been notified that their registration has been completed."
        ),
    )

    # custom managers
    objects = models.Manager()
    completed_registrations = CompletedRegistrationManager()
    todo_registrations = NotCompletedRegistrationManager()

    class Meta:
        verbose_name = _("Student Registration")
        verbose_name_plural = _("Student Registration")
        ordering = ("slack_registered", "sds_registered", "-date_registered")
        get_latest_by = "date_registered"

    def completed_registration(self):
        """
        Determines if this student has completed the registration process. This method is used in every step in the
        registration process from sending notification emails to administrative views, and ultimately controls if the
        user can log into CodeDevils services. Change the logic of this method to determine how a user is considered
        registered.

        Registration is complete as soon as the user is registered on Slack and SunDevilSync.
        """
        return self.slack_registered and self.sds_registered

    def __str__(self):
        return f"{self.user.name} [done: {self.completed_registration()}]"

    def save(
        self, admin_view_change=False, restart_registration=False, *args, **kwargs
    ):
        """Sets SDS registration to True if the user is registering as alumni."""
        if self.user.is_alumni and not admin_view_change:
            self.sds_registered = self.sds_notified = True
        self._admin_view_change = admin_view_change
        self._restart_registration = restart_registration
        super().save(*args, **kwargs)


class KnownMember(RegistrationModelAbstract):
    """
    Separate listing of known members who exist either in SunDevilSync or Slack but have not created accounts
    with CodeDevils yet.
    """

    email = models.EmailField(
        db_column="Email", blank=False, null=False, verbose_name=_("Email")
    )
    name = models.CharField(
        db_column="Name", blank=True, max_length=255, verbose_name=_("Name of member")
    )
    slack_id = models.CharField(
        db_column="SlackId", blank=True, max_length=12, verbose_name=_("Slack ID")
    )
    tz_offset = models.IntegerField(
        db_column="TzOffset",
        blank=True,
        null=True,
        default=0,
        verbose_name=_("UTC Offset"),
        validators=[MinValueValidator(-43200), MaxValueValidator(54000)],
        help_text=_("UTC offset in seconds"),
    )
    image_24 = models.URLField(
        db_column="Image24",
        blank=True,
        verbose_name=_("Image 24"),
        help_text=_("User 24px profile image"),
    )
    image_512 = models.URLField(
        db_column="Image512",
        blank=True,
        verbose_name=_("Image 512"),
        help_text=_("User 512px profile image"),
    )

    class Meta:
        verbose_name = _("Known Member")
        verbose_name_plural = _("Known Members")
        ordering = ("slack_registered", "sds_registered", "email")
