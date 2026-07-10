from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import Employee
from django.contrib import messages
from .forms import EmployeeForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def employee_list(request):

    search = request.GET.get("search", "").strip()

    employees = Employee.objects.select_related(
        "department",
    )

    if search:

        employees = employees.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    paginator = Paginator(
        employees,
        10,
    )

    page_number = request.GET.get("page")

    employees = paginator.get_page(
        page_number,
    )

    context = {
        "employees": employees,
        "search": search,
    }

    return render(
        request,
        "employees/employee_list.html",
        context,
    )

@login_required
def employee_create(request):

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES,
        )

        if request.method == "POST":

            form = EmployeeForm(
                request.POST,
                request.FILES,
            )

            if form.is_valid():

                form.save()

                messages.success(
                    request,
                    "Employee added successfully."
                )

                return redirect("employee-list")

            print(form.errors)

    else:

        form = EmployeeForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "employees/employee_form.html",
        context,
    )

@login_required
def employee_update(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk,
    )

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Employee updated successfully."
            )

            return redirect("employee-list")

    else:

        form = EmployeeForm(
            instance=employee,
        )

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "employee": employee,
        },
    )

@login_required
def employee_delete(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk,
    )

    if request.method == "POST":

        employee.delete()

        messages.success(
            request,
            "Employee deleted successfully."
        )

        return redirect("employee-list")

    return render(
        request,
        "employees/employee_confirm_delete.html",
        {
            "employee": employee,
        },
    )