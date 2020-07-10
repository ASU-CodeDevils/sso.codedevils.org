from rest_framework import serializers

from cdsso.contrib.register.models import StudentRegistration


class StudentRegistrationSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentRegistration
        fields = "__all__"
        description = "Steps completed in the registration process"

    def get_completed(self, obj: StudentRegistration):
        """Whether or not this user has completed the registration process."""
        return obj.completed_registration()
