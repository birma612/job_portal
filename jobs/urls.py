
from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    MyApplicationsView,
    apply_job,
    create_job,
    EmployerDashboardView,
    edit_job,
    delete_job,
    job_applicants,
)

urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),

    path('create/', create_job, name='create-job'),

    path(
        'employer-dashboard/',
        EmployerDashboardView.as_view(),
        name='employer-dashboard',
    ),

    path('<int:pk>/edit/', edit_job, name='edit-job'),

    path('<int:pk>/apply/', apply_job, name='apply-job'),

    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),

    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
  path('<int:pk>/delete/', delete_job, name='delete-job'),
  path('<int:pk>/applicants/', job_applicants, name='job-applicants'),
]
