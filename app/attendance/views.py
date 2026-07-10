from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import AttendanceForm
from .models import Attendance
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from employees.models import Employee
from django.contrib import messages
from datetime import datetime
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)


@login_required
def attendance_list(request):

    search = request.GET.get(
        "search",
        "",
    ).strip()

    date = request.GET.get(
        "date",
        "",
    ).strip()

    attendances = Attendance.objects.select_related(
        "employee",
    )

    # Search

    if search:

        attendances = attendances.filter(

            Q(employee__employee_id__icontains=search)

            | Q(employee__first_name__icontains=search)

            | Q(employee__last_name__icontains=search)

        )

    # Date Filter

    if date:

        attendances = attendances.filter(
            date=date,
        )

    # Summary Counts

    present_count = attendances.filter(
        status="Present"
    ).count()

    late_count = attendances.filter(
        status="Late"
    ).count()

    leave_count = attendances.filter(
        status="Leave"
    ).count()

    absent_count = attendances.filter(
        status="Absent"
    ).count()

    # Latest First

    attendances = attendances.order_by(
        "-date",
        "-id",
    )

    # Pagination

    paginator = Paginator(
        attendances,
        10,
    )

    page_number = request.GET.get(
        "page",
    )

    attendances = paginator.get_page(
        page_number,
    )

    context = {

        "attendances": attendances,

        "search": search,

        "date": date,

        "present_count": present_count,

        "late_count": late_count,

        "leave_count": leave_count,

        "absent_count": absent_count,

    }

    return render(

        request,

        "attendance/attendance_list.html",

        context,

    )

@login_required
def attendance_create(request):

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance marked successfully.",
            )

            return redirect(
                "attendance-list",
            )

    else:

        form = AttendanceForm()

    context = {

        "form": form,

    }

    return render(

        request,

        "attendance/attendance_form.html",

        context,

    )

@login_required
def attendance_update(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
            instance=attendance,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance updated successfully.",
            )

            return redirect(
                "attendance-list",
            )

    else:

        form = AttendanceForm(
            instance=attendance,
        )

    return render(

        request,

        "attendance/attendance_form.html",

        {

            "form": form,

        },

    )

@login_required
def attendance_delete(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    if request.method == "POST":

        attendance.delete()

        messages.success(
            request,
            "Attendance deleted successfully.",
        )

        return redirect(
            "attendance-list",
        )

    return render(
        request,
        "attendance/attendance_confirm_delete.html",
        {
            "attendance": attendance,
        },
    )

@login_required
def attendance_detail(request, pk):

    attendance = get_object_or_404(
        Attendance.objects.select_related(
            "employee",
        ),
        pk=pk,
    )

    context = {

        "attendance": attendance,

    }

    return render(

        request,

        "attendance/attendance_detail.html",

        context,

    )

@login_required
def bulk_attendance_create(request):

    selected_date = request.GET.get(
        "date",
    )

    attendance_map = {}

    if request.method == "POST":

        attendance_date = request.POST.get(
            "date"
        )

        employees = Employee.objects.filter(
            status="Active"
        ).order_by(
            "employee_id"
        )


        for employee in employees:

            status = request.POST.get(
                f"status_{employee.id}"
            )

            check_in = request.POST.get(
                f"check_in_{employee.id}"
            )

            check_out = request.POST.get(
                f"check_out_{employee.id}"
            )

            Attendance.objects.update_or_create(

                employee=employee,

                date=attendance_date,

                defaults={

                    "status": status,

                    "check_in": check_in if check_in else None,

                    "check_out": check_out if check_out else None,

                }

            )

        messages.success(

            request,

            "Bulk attendance saved successfully."

        )

        return redirect(
            "attendance-list"
        )

    employees = Employee.objects.filter(
        status="Active",
    ).order_by(
        "employee_id",
    )

    if selected_date:

        employees = Employee.objects.filter(
            status="Active",
        ).order_by(
            "employee_id",
        )

        attendances = Attendance.objects.filter(
            date=selected_date,
        )

        attendance_map = {

            attendance.employee_id: attendance

            for attendance in attendances

        }

    else:

        employees = Employee.objects.none()
        
    context = {

        "employees": employees,

        "selected_date": selected_date,

        "attendance_map": attendance_map,

    }

    return render(

        request,

        "attendance/bulk_attendance.html",

        context,

    )