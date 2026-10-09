from django.contrib import admin
from .models import job, Application


class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'company_name',
        'location',
        'salary',
        'posted_by',
        'date_posted'
    ]

    search_fields = ['title', 'company_name']
    list_filter = ['location']


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)