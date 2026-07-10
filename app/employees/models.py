from django.db import models
from departments.models import Department


class Employee(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    employee_id = models.CharField(
        max_length=10,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        unique=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    joining_date = models.DateField()

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active"
    )

    profile_picture = models.ImageField(
        upload_to="employees/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"