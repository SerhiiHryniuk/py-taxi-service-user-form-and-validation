from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from taxi.models import Driver


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "license_number")
        help_texts = {
            "license_number": mark_safe(
                "<ul>"
                    "<li>Your license number should only consist of 8 characters long.</li>"
                    "<li>Your license number's first 3 characters are uppercase letters.</li>"
                    "<li>Your license number's last 5 characters are digits.</li>"
                "</ul>"
            )
        }

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != 8:
            raise ValidationError(
                f"Ensure that license number should consist of exactly 8 characters."
            )

        if not (license_number[:3].isupper() and license_number[:3].isalpha()):
            raise ValidationError(
                f"Ensure that first 3 characters are uppercase letters."
            )

        if not license_number[-5:].isdigit():
            raise ValidationError(
                f"Ensure that last 5 characters are digits."
            )

        return license_number