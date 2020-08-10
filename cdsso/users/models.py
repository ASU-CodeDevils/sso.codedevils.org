from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class StudentManager(models.Manager):
    """Manager for the user model that selects only active students."""

    def get_queryset(self):
        queryset = super(StudentManager, self).get_queryset()
        queryset = queryset.filter(is_alumni=False, is_active=True)
        return queryset


class AlumniManager(models.Manager):
    """Manager for the user models that selects only alumni (active or not)."""

    def get_queryset(self):
        queryset = super(AlumniManager, self).get_queryset()
        queryset = queryset.filter(is_alumni=True)
        return queryset


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    anonymous = models.BooleanField(
        db_column="IsAnonymous",
        default=True,
        blank=False,
        null=False,
        verbose_name=_("Anonymous"),
        help_text=_(
            "You have the option of keeping your account anonymous with CD. "
            "Selecting this will ensure your account stays private and supported "
            "applications don't have access to your data"
        ),
    )
    receive_notifications = models.BooleanField(
        db_column="ReceiveNotifications",
        default=True,
        verbose_name=_("Receive notifications"),
        help_text="Receive emails about the latest and greatest at CodeDevils!",
    )
    is_alumni = models.BooleanField(
        db_column="IsStudent",
        null=False,
        default=False,
        verbose_name=_("Is an alumni"),
        help_text=_("Is an alumni of ASU. If False, the user is by default a student."),
    )

    # managers
    objects = UserManager()
    students = StudentManager()
    alumni = AlumniManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.username})"
        return f"{self.username}"
