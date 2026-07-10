from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Leave


class LeaveForm(forms.ModelForm):

    class Meta:

        model = Leave

        fields = [
            "employee",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
        ]

        widgets = {

            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if name in ["employee", "leave_type", "status"]:

                field.widget.attrs["class"] = "form-select"

            else:

                field.widget.attrs["class"] = "form-control"
    
    def clean(self):

        cleaned_data = super().clean()

        employee = cleaned_data.get("employee")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        status = cleaned_data.get("status")

        if start_date and end_date:

            if end_date < start_date:

                self.add_error(
                    "end_date",
                    "End date must be after start date."
                )

        if start_date:

            if start_date < timezone.localdate():

                self.add_error(
                    "start_date",
                    "Past leave cannot be applied."
                )

        if employee and start_date and end_date:

            leave = Leave.objects.filter(
                employee=employee,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )

            if self.instance.pk:

                leave = leave.exclude(
                    pk=self.instance.pk,
                )

            if leave.exists():

                raise ValidationError(
                    "This employee already has a leave within the selected date range."
                )