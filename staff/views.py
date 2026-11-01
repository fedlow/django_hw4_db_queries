from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Employee


class HomePageView(ListView):
    model = Employee
    template_name = "staff/home.html"
    context_object_name = "employees"

    def get_queryset(self):
        return Employee.objects.order_by("-hire_date")[:4].prefetch_related("images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_employees"] = Employee.objects.count()
        return context


class EmployeeListView(ListView):
    model = Employee
    template_name = "staff/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        return Employee.objects.all().prefetch_related("images")


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "staff/employee_detail.html"
    context_object_name = "employee"

    def get_queryset(self):
        return Employee.objects.prefetch_related("images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = self.object.images.all()
        context["main_image"] = images.first()
        context["other_images"] = images[1:]
        return context
