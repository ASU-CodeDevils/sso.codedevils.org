from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class StudentRegistrationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {
            "duplicate_username": _("This username has already been taken."),
            "invalid_email": _("Please enter a valid email address"),
            "duplicate_email": _("This email has already been taken."),
            "student_email_required": _("Please enter your ASU email."),
            "alumni_email_required": _("You are applying as an alumni and cannot use your student email"),
            "student_email_asurite": _("Please enter your ASURITE email (<ASURITE>@asu.edu)")
        }
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ["username", "password1", "password2", "email", "anonymous", "receive_notifications", "is_alumni"]
        labels = {"is_alumni": "Alumni"}
        help_texts = {
            "receive_notifications": "We will send you emails about events, exciting new projects and opportunities, "
                                     "and different ways to get involved in CodeDevils",
            "is_alumni": "Check here if you are an alumni. We will get you in contact with an Officer to help set "
                         "you up",
            "anonymous": "You can opt to be anonymous, which means we will block your information publicly and "
                         "limit it between different CodeDevils products."
        }

    def clean_email(self):
        """Determines if the email is valid based on if the user is a student or alumni."""
        email = self.cleaned_data["email"]
        is_alumni = self.cleaned_data.get("is_alumni", False)

        # check that the email is valid
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(self.error_messages["invalid_email"])

        # if a student, their email must end in asu.edu and be their asurite
        split_email = email.split("@")  # split email by username and domain
        if not is_alumni:
            # email must end in asu.edu
            if split_email[1] != "asu.edu":
                raise ValidationError(self.error_messages["student_email_required"])

            # ASURITE is 5-8 characters long
            if len(split_email[0]) < 5 or len(split_email[0]) > 8:
                raise ValidationError(self.error_messages["student_email_asurite"])
        else:
            if split_email[1] == "asu.edu":
                raise ValidationError(self.error_messages["alumni_email_required"])

        # check that the email is not already assigned to an account
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])

    def clean_username(self):
        """Ensures the username has not been used yet."""
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])
