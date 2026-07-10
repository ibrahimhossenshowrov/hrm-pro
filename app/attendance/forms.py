from django import forms
from .models import Attendance
from django.core.exceptions import ValidationError
from django.utils import timezone


class AttendanceForm(forms.ModelForm):

    class Meta:

        model = Attendance

        fields = [
            "employee",
            "date",
            "check_in",
            "check_out",
            "status",
        ]

        widgets = {

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "check_in": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "check_out": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control",
                }
            ),

            "employee": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():

            if field_name not in [
                "employee",
                "status",
                "date",
                "check_in",
                "check_out",
            ]:

                field.widget.attrs["class"] = "form-control"

    def clean(self):

        cleaned_data = super().clean()

        employee = cleaned_data.get("employee")
        date = cleaned_data.get("date")
        status = cleaned_data.get("status")
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if date and date > timezone.localdate():

            raise ValidationError(
                "Future attendance cannot be added."
            )

        if check_in and check_out:

            if check_out <= check_in:

                raise ValidationError(
                    "Check out time must be later than check in time."
                )

        # Present / Late / Half Day হলে Check In এবং Check Out required

        if status in ["Present", "Late", "Half Day"]:

            if not check_in:

                self.add_error(
                    "check_in",
                    "Check in time is required."
                )

            if not check_out:

                self.add_error(
                    "check_out",
                    "Check out time is required."
                )
                
        # Leave / Absent হলে time দেওয়া যাবে না

        if status in ["Leave", "Absent"]:

            if check_in:

                self.add_error(
                    "check_in",
                    "Check in is not allowed for this status."
                )

            if check_out:

                self.add_error(
                    "check_out",
                    "Check out is not allowed for this status."
                )