from django.urls import path
from . import views

urlpatterns = [
    path("", views.employee_list, name="employee-list"),

    path(
        "add/",
        views.employee_create,
        name="employee-create",
    ),

    path(
    "<int:pk>/edit/",
    views.employee_update,
    name="employee-update",
    ),

    path(
    "<int:pk>/delete/",
    views.employee_delete,
    name="employee-delete",
    ),
]
