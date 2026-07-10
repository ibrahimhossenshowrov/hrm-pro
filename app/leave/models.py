from django.db import models

from employees.models import Employee


class Leave(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    LEAVE_TYPE_CHOICES = [
        ("Casual", "Casual"),
        ("Sick", "Sick"),
        ("Annual", "Annual"),
        ("Unpaid", "Unpaid"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leaves",
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE_CHOICES,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"