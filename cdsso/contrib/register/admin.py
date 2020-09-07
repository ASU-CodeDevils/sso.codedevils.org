from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cdsso.contrib.register.models import KnownMember, StudentRegistration


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ["user", "completed_registration"]
    search_fields = [
        "user",
        "slack_registered",
        "sds_registered",
        "completed_registration",
    ]

    def completed_registration(self, obj):
        return obj.completed_registration()

    completed_registration.short_description = _("Completed Registration")


@admin.register(KnownMember)
class KnownMemberAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "slack_registered", "sds_registered"]
    search_fields = ["email", "name", "slack_registered", "sds_registered"]
