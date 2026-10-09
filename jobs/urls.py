from django.urls import path
from .views import JobListView, JobDetailView, MyApplicationsView, apply_job

urlpatterns = [
    path('', JobListView.as_view(), name='job-list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('<int:pk>/apply/', apply_job, name='apply-job'),
    path('my-applications/', MyApplicationsView.as_view(), name='my-applications'),
]