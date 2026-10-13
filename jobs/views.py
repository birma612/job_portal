from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import job, Application
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import JobForm
from django.views.generic import TemplateView
from .models import job


# class JobListView(ListView):
#     model = job
#     template_name = 'jobs/job_list.html'
#     context_object_name = 'all_jobs'


class JobListView(ListView):
    model = job
    template_name = 'jobs/job_list.html'
    context_object_name = 'all_jobs'

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('q', '').strip()
        location_query = self.request.GET.get('location', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(company_name__icontains=search_query)
            )

        if location_query:
            queryset = queryset.filter(
                location__icontains=location_query
            )

        sort_by = self.request.GET.get('sort', 'newest')
        sort_options = {
            'newest': '-date_posted',
            'oldest': 'date_posted',
            'salary_high': '-salary',
            'salary_low': 'salary',
        }

        queryset = queryset.order_by(
            sort_options.get(sort_by, '-date_posted')
        )

        return queryset


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
def create_job(request):
    if request.user.role != 'employer':
        raise PermissionDenied(
            "Only employers can create job postings."
        )

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.posted_by = request.user
            job_post.save()

            messages.success(
                request,
                'Your job posting has been created successfully.'
            )
            return redirect('job-list')
    else:
        form = JobForm()

    return render(
        request,
        'jobs/create_job.html',
        {'form': form}
    )
    
    

@login_required
def edit_job(request, pk):
    if request.user.role != 'employer':
        raise PermissionDenied(
            "Only employers can edit job postings."
        )

    job_instance = get_object_or_404(
        job,
        pk=pk,
        posted_by=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job_instance)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your job posting has been updated successfully.'
            )
            return redirect('employer-dashboard')
    else:
        form = JobForm(instance=job_instance)

    return render(
        request,
        'jobs/edit_job.html',
        {'form': form, 'job': job_instance}
    )

   
    

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
class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'
    login_url = '/accounts/login/'

    def get_queryset(self):
        return Application.objects.filter(
            applicant=self.request.user
        ).select_related('job')
        
        

class EmployerDashboardView(LoginRequiredMixin, ListView):
    model = job
    template_name = 'jobs/employer_dashboard.html'
    context_object_name = 'my_jobs'
    login_url = '/accounts/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role != 'employer':
            raise PermissionDenied(
                "Only employers can access the employer dashboard."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return job.objects.filter(
            posted_by=self.request.user
        ).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_jobs'] = self.get_queryset().count()
        context['total_applications'] = Application.objects.filter(
            job__posted_by=self.request.user
        ).count()
        return context
        
            

@login_required
def delete_job(request, pk):
    if request.user.role != 'employer':
        raise PermissionDenied(
            "Only employers can delete job postings."
        )

    job_instance = get_object_or_404(
        job,
        pk=pk,
        posted_by=request.user
    )

    if request.method == 'POST':
        job_title = job_instance.title
        job_instance.delete()

        messages.success(
            request,
            f'Job "{job_title}" has been deleted successfully.'
        )
        return redirect('employer-dashboard')

    return render(
        request,
        'jobs/delete_job.html',
        {'job': job_instance}
    )

@login_required
def job_applicants(request, pk):
    if request.user.role != 'employer':
        raise PermissionDenied(
            "Only employers can view job applicants."
        )

    job_instance = get_object_or_404(
        job,
        pk=pk,
        posted_by=request.user
    )

    applications = Application.objects.filter(
        job=job_instance
    ).select_related('applicant').order_by('applicant__username')

    return render(
        request,
        'jobs/job_applicants.html',
        {
            'job': job_instance,
            'applications': applications,
            'total_applicants': applications.count(),
        }
    )



class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["latest_jobs"] = job.objects.order_by(
            "-date_posted"
        )[:6]

        context["total_jobs"] = job.objects.count()

        return context
