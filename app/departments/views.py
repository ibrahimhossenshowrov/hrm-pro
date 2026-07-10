from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Department
from .forms import DepartmentForm
from django.db.models import Q
from django.core.paginator import Paginator

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10 

    def get_queryset(self):

        search = self.request.GET.get(
            "search",
            "",
        ).strip()

        queryset = Department.objects.all()

        if search:

            queryset = queryset.filter(

                Q(name__icontains=search) |

                Q(description__icontains=search)

            )

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["search"] = self.request.GET.get(
            "search",
            "",
        )

        return context

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department-list')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department-list')

from django.contrib import messages
from django.shortcuts import redirect

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):

    model = Department
    template_name = "departments/confirm_delete.html"
    success_url = reverse_lazy("department-list")

    def form_valid(self, form):

        self.object = self.get_object()

        if self.object.employees.exists():

            messages.error(
                self.request,
                "This department cannot be deleted because employees are assigned to it."
            )

            return redirect("department-list")


        return super().form_valid(form)