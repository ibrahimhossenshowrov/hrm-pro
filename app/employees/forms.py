from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee

        fields = [
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "date_of_birth",
            "joining_date",
            "department",
            "salary",
            "status",
            "profile_picture",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),

            "joining_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if name == "department":

                field.widget.attrs["class"] = "form-select"

            else:

                field.widget.attrs["class"] = "form-control"