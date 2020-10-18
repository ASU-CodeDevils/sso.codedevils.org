from rest_framework import serializers

from cdsso.contrib.register.models import KnownMember, StudentRegistration


class StudentRegistrationSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = StudentRegistration
        fields = "__all__"
        description = "Steps completed in the registration process"

    def get_completed(self, obj: StudentRegistration):
        """Whether or not this user has completed the registration process."""
        return obj.completed_registration()


class KnownMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnownMember
        fields = "__all__"
        description = (
            "All known members that have not completed the online registration."
        )


# ------------------------------------------------------
# Below are specific to Flameboi and are used to format the request body


class SlackUserProfileSerializer(serializers.Serializer):
    title = serializers.CharField()
    phone = serializers.CharField()
    skype = serializers.CharField()
    real_name = serializers.CharField()
    real_name_normalized = serializers.CharField()
    display_name = serializers.CharField()
    display_name_normalized = serializers.CharField()
    fields = serializers.ListField(default=None)
    status_text = serializers.CharField(default="")
    status_emoji = serializers.CharField(default="")
    status_expiration = serializers.IntegerField(default=0)
    avatar_hash = serializers.CharField()
    image_original = serializers.URLField()
    is_custom_image = serializers.BooleanField()
    email = serializers.CharField(required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image_24 = serializers.URLField()
    image_32 = serializers.URLField()
    image_48 = serializers.URLField()
    image_72 = serializers.URLField()
    image_192 = serializers.URLField()
    image_512 = serializers.URLField()
    image_1024 = serializers.URLField()
    status_text_canonical = serializers.CharField(default=None)
    team = serializers.CharField(default=None)


class SlackEnterpriseUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    enterprise_id = serializers.CharField()
    enterprise_name = serializers.CharField()
    is_admin = serializers.BooleanField()
    is_owner = serializers.BooleanField()
    teams = serializers.DictField()


class SlackUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    team_id = serializers.CharField()
    name = serializers.CharField()
    deleted = serializers.BooleanField()
    color = serializers.CharField()
    real_name = serializers.CharField()
    tz = serializers.CharField()
    tz_label = serializers.CharField()
    tz_offset = serializers.IntegerField()
    profile = SlackUserProfileSerializer(required=True)
    is_admin = serializers.BooleanField()
    is_owner = serializers.BooleanField()
    is_primary_owner = serializers.BooleanField()
    is_restricted = serializers.BooleanField()
    is_ultra_restricted = serializers.BooleanField()
    is_bot = serializers.BooleanField()
    is_stranger: serializers.BooleanField()
    is_invited_user = serializers.BooleanField()
    is_app_user = serializers.BooleanField()
    updated = serializers.IntegerField()
    has_2fa = serializers.BooleanField()
    locale = serializers.CharField()


class SlackUserObjectSerializer(serializers.Serializer):
    ok = serializers.BooleanField(required=False)
    user = SlackUserSerializer(required=True, many=False)
    enterprise_user = SlackEnterpriseUserSerializer(required=False, many=False)


class SlackResponseSerializer(serializers.Serializer):
    ok = serializers.BooleanField(default=True)
    created = serializers.BooleanField(
        required=False,
        help_text="true if the user has not started the registration process",
    )
    detail = serializers.CharField(default="user registered on slack")


class SlackErrorResponseSerializer(serializers.Serializer):
    ok = serializers.BooleanField(default=False)
    detail = serializers.CharField(default="invalid format")
    key = serializers.CharField(
        required=False,
        help_text="Identifies the missing key if invalid format is raised",
    )
