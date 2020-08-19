from rest_framework import serializers

from cdsso.contrib.register.models import KnownMember, StudentRegistration


class StudentRegistrationSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField(read_only=True)

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
        description = "All known members that have not completed the online registration."
