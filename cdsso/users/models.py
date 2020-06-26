from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    anonymous = models.BooleanField(db_column="IsAnonymous", default=True, blank=False, null=False,
                                    verbose_name=_("Anonymous"),
                                    help_text=_("You have the option of keeping your account anonymous with CD. "
                                                "Selecting this will ensure your account stays private and supported "
                                                "applications don't have access to your data"))

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.username})"
        return f"{self.username}"
