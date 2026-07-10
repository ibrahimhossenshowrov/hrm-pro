from django.urls import path
from . import views

urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department-list'),
    path('create/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department-edit'),
    path('<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department-delete'),
]