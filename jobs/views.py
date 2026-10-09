from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import job, Application


class JobListView(ListView):
    model = job
    template_name = 'jobs/job_list.html'
    context_object_name = 'all_jobs'


class JobDetailView(DetailView):
    model = job
    template_name = 'jobs/job_details.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['already_applied'] = Application.objects.filter(
                job=self.object,
                applicant=self.request.user
            ).exists()
        else:
            context['already_applied'] = False

        return context

@login_required
def apply_job(request, pk):
    job_instance = get_object_or_404(job, pk=pk)

    if Application.objects.filter(
        job=job_instance,
        applicant=request.user
    ).exists():
        messages.info(request, 'You have already applied for this job.')
        return redirect('job-detail', pk=job_instance.pk)

    Application.objects.create(
        job=job_instance,
        applicant=request.user
    )

    messages.success(request, 'Your application has been submitted successfully.')

    return redirect('job-detail', pk=job_instance.pk)
class MyApplicationsView(ListView):
    model = Application
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job')