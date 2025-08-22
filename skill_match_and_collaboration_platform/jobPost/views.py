from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import JobPost
from .forms import JobPostForm

@method_decorator(login_required, name='dispatch')
class AddJobPostView(CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'add_jobPost.html'
    success_url = reverse_lazy('homepage')  # Redirect after successful creation

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as the author
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditJobPostView(UpdateView):
    model = JobPost
    form_class = JobPostForm
    template_name = 'add_jobPost.html'
    success_url = reverse_lazy('homepage')  # Redirect after successful edit
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure author remains the logged-in user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeleteJobPostView(DeleteView):
    model = JobPost
    template_name = 'confirm_delete_job_post.html'  # Template to confirm deletion
    success_url = reverse_lazy('homepage')  # Redirect after successful deletion
    pk_url_kwarg = 'id'


def detail(request, id):
    job = get_object_or_404(JobPost, pk=id)
    form = ApplicationForm()
    return render(request, 'details.html', {'job': job, 'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import JobPost, Application, Notification
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required

# Job Detail View
# @login_required
# def job_detail(request, id):
#     job = get_object_or_404(JobPost, id=id)
#     applications = job.application_set.all()
#     user_application = None

#     if job.application_set.filter(author=request.user).exists():
#         user_application = job.application_set.get(author=request.user)

#     return render(request, 'job_detail.html', {
#         'job': job,
#         'applications': applications,
#         'user_application': user_application,
#     })

@login_required
def application_detail_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Ensure only the applicant or the job post author can view the application details
    if application.author != request.user and application.JobPost.author != request.user:
        return redirect('homepage')

    return render(request, 'application_detail.html', {'application': application})

# Application View
@login_required
def application_view(request, id):
    job = get_object_or_404(JobPost, id=id)

    if job.author == request.user:
        return redirect('job_detail', id=id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.JobPost = job
            application.author = request.user
            application.save()

            Notification.objects.create(
                application=application,
                recipient=job.author,
                message=f"New application from {application.full_name} for {job.title}."
            )
            return redirect('homepage')
    else:
        form = ApplicationForm()

    return render(request, 'applicationForm.html', {'form': form, 'job': job})

# Manage Application View
@login_required
def manage_application(request, application_id, action):
    application = get_object_or_404(Application, id=application_id)

    # Ensure only the JobPost author can manage the application
    if request.user != application.JobPost.author:
        return redirect('homepage')

    if action == "accept":
        job = application.JobPost
        job.status = 'Find'
        job.save()

        application.status = 'Accepted'
        application.save()

        # Create a notification for the applicant
        Notification.objects.create(
            application=application,
            recipient=application.author,
            message=f"Your application for {application.JobPost.title} has been accepted."
        )

    elif action == "reject":
        application.status = 'Rejected'
        application.save()

        # Create a notification for the applicant
        Notification.objects.create(
            application=application,
            recipient=application.author,
            message=f"Your application for {application.JobPost.title} has been rejected."
        )

    return redirect('homepage')

# Notifications View
@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    notifications.update(is_read=True)
    return render(request, 'notifications.html', {'notifications': notifications})