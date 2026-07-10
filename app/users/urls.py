from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.login_view, name="login"),
    path("forgot-password/", views.forgot_password_view, name="forgot-password"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("logout/", views.logout_view, name="logout"),

]