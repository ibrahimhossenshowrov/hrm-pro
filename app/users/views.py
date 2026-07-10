from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.messages import get_messages


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")
    
    storage = get_messages(request)

    for _ in storage:
        pass

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome, {user.username}!"
                )

                return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "Invalid username or password."
                )

    return render(
        request,
        "users/login.html",
        {
            "form": form
        }
    )

@login_required
def dashboard(request):

    return render(
        request,
        "users/dashboard.html"
    )


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")

def forgot_password_view(request):
    return render(request, "users/forgot-password.html")
    