from rest_framework import serializers

from cdsso.contrib.register.api.serializers import StudentRegistrationSerializer
from cdsso.users.models import User

USER_EXCLUDE_FIELDS = (
    "password",
    "groups",
    "user_permissions",
    "is_staff",
    "is_superuser",
)


class UserSerializer(serializers.ModelSerializer):
    registration = StudentRegistrationSerializer(many=False, read_only=True)

    class Meta:
        model = User
        exclude = USER_EXCLUDE_FIELDS

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
