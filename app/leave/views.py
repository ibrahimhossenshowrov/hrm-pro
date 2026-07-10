from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Leave
from .forms import LeaveForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


@login_required
def leave_list(request):

    search = request.GET.get(
        "search",
        "",
    ).strip()

    status = request.GET.get(
        "status",
        "",
    ).strip()

    leaves = Leave.objects.select_related(
        "employee",
    )

    pending_count = leaves.filter(
        status="Pending"
    ).count()

    approved_count = leaves.filter(
        status="Approved"
    ).count()

    rejected_count = leaves.filter(
        status="Rejected"
    ).count()

    total_count = leaves.count()

    if search:

        leaves = leaves.filter(

            Q(employee__employee_id__icontains=search) |

            Q(employee__first_name__icontains=search) |

            Q(employee__last_name__icontains=search)

        )

    if status:

        leaves = leaves.filter(
            status=status,
        )

    paginator = Paginator(
        leaves,
        10,
    )

    page_number = request.GET.get(
        "page",
    )

    leaves = paginator.get_page(
        page_number,
    )

    context = {

        "leaves": leaves,
        "search": search,
        "status": status,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "total_count": total_count,

    }

    return render(

        request,

        "leave/leave_list.html",

        context,

    )

@login_required
def leave_approve(request, pk):

    leave = get_object_or_404(
        Leave,
        pk=pk,
    )

    leave.status = "Approved"

    leave.save()

    messages.success(

        request,

        "Leave approved successfully."

    )

    return redirect(
        "leave-list",
    )

@login_required
def leave_reject(request, pk):

    leave = get_object_or_404(
        Leave,
        pk=pk,
    )

    leave.status = "Rejected"

    leave.save()

    messages.success(

        request,

        "Leave rejected successfully."

    )

    return redirect(
        "leave-list",
    )

@login_required
def leave_create(request):

    if request.method == "POST":

        form = LeaveForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Leave applied successfully."
            )

            return redirect(
                "leave-list"
            )

    else:

        form = LeaveForm()

    context = {

        "form": form,

    }

    return render(

        request,

        "leave/leave_form.html",

        context,

    )

@login_required
def leave_detail(request, pk):

    leave = get_object_or_404(

        Leave.objects.select_related(
            "employee",
        ),

        pk=pk,

    )

    context = {

        "leave": leave,

    }

    return render(

        request,

        "leave/leave_detail.html",

        context,

    )

@login_required
def leave_update(request, pk):

    leave = get_object_or_404(
        Leave,
        pk=pk,
    )

    if request.method == "POST":

        form = LeaveForm(
            request.POST,
            instance=leave,
        )

        if leave.status != "Pending":

            messages.error(

                request,

                "Only pending leave requests can be edited."

            )

            return redirect(
                "leave-detail",
                pk=leave.pk,
            )

        if form.is_valid():

            form.save()

            return redirect(
                "leave-list",
            )

    else:

        form = LeaveForm(
            instance=leave,
        )

    context = {

        "form": form,

    }

    return render(

        request,

        "leave/leave_form.html",

        context,

    )

@login_required
def leave_delete(request, pk):

    leave = get_object_or_404(
        Leave,
        pk=pk,
    )

    if request.method == "POST":

        leave.delete()

        return redirect(
            "leave-list",
        )

    context = {

        "leave": leave,

    }

    return render(

        request,

        "leave/leave_confirm_delete.html",

        context,

    )

