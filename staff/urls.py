from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("employees/", views.EmployeeListView.as_view(), name="employee_list"),
    path(
        "employees/<int:pk>/",
        views.EmployeeDetailView.as_view(),
        name="employee_detail",
    ),
]
