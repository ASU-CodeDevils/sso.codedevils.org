from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cdsso.contrib.register.models import KnownMember, StudentRegistration


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ["user", "slack_registered", "sds_registered", "completed_registration"]
    list_filter = ["slack_registered", "sds_registered"]
    search_fields = ["user"]

    def completed_registration(self, obj):
        return obj.completed_registration()

    completed_registration.short_description = _("Completed Registration")


@admin.register(KnownMember)
class KnownMemberAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "slack_registered", "sds_registered"]
    list_filter = ["slack_registered", "sds_registered"]
    search_fields = ["email", "name"]
