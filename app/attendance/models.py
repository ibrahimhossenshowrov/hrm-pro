from django.db import models
from employees.models import Employee


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Late", "Late"),
        ("Absent", "Absent"),
        ("Half Day", "Half Day"),
        ("Leave", "Leave"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    date = models.DateField()

    check_in = models.TimeField(
        blank=True,
        null=True,
    )

    check_out = models.TimeField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Present",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-date",
            "employee__first_name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "employee",
                    "date",
                ],
                name="unique_employee_attendance",
            ),
        ]

    def __str__(self):

        return f"{self.employee} - {self.date}"