from django.shortcuts import render
from django.http import JsonResponse
from jobPost.models import JobPost
from Categories.models import Categories
from django.template.loader import render_to_string

def find_job(request):
    jobs = JobPost.objects.all()
    categories = Categories.objects.all()
    job_types = dict(JobPost.JOB_TYPES)
    return render(request, 'findjob.html', {'data': jobs, 'categories': categories, 'job_types': job_types})

def filter_jobs(request):
    categories = request.GET.getlist('category[]')
    job_types = request.GET.getlist('job_type[]')

    jobs = JobPost.objects.all()

    if categories:
        jobs = jobs.filter(Categories__id__in=categories).distinct()
    if job_types:
        jobs = jobs.filter(job_type__overlap=job_types)  # MultiSelectField filtering

    html = render_to_string("ajax/job-list.html", {"data": jobs})
    return JsonResponse({"data": html})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')