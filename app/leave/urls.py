from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.leave_list,
        name="leave-list",
    ),

    path(
        "create/",
        views.leave_create,
        name="leave-create",
    ),

    path(
        "",
        views.leave_list,
        name="leave-list",
    ),

    path(
        "<int:pk>/",
        views.leave_detail,
        name="leave-detail",
    ),

    path(
        "<int:pk>/edit/",
        views.leave_update,
        name="leave-edit",
    ),

    path(
        "<int:pk>/delete/",
        views.leave_delete,
        name="leave-delete",
    ),

    path(
        "<int:pk>/approve/",
        views.leave_approve,
        name="leave-approve",
    ),

    path(
        "<int:pk>/reject/",
        views.leave_reject,
        name="leave-reject",
    ),
]