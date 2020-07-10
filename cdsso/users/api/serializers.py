from rest_framework import serializers

from cdsso.contrib.register.api.serializers import StudentRegistrationSerializer
from cdsso.users.models import User


class UserSerializer(serializers.ModelSerializer):
    registration = StudentRegistrationSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "name", "url", "anonymous", "registration"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }
