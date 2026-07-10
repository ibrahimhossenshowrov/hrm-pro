from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.attendance_list,
        name="attendance-list",
    ),
    path(
        "create/",
        views.attendance_create,
        name="attendance-create",
    ),
    path(
        "<int:pk>/edit/",
        views.attendance_update,
        name="attendance-update",
    ),
    path(
        "<int:pk>/delete/",
        views.attendance_delete,
        name="attendance-delete",
    ),
    path(
        "<int:pk>/",
        views.attendance_detail,
        name="attendance-detail",
    ),

    path(
        "bulk-create/",
        views.bulk_attendance_create,
        name="attendance-bulk-create",
    ),
]