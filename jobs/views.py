from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Application
from .forms import JobForm, ApplicationForm

# Home Page
def home(request):
    return render(request, 'home.html')

# Job Listing
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# Job Detail
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

# Organization Dashboard
@login_required
def organization_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)  # Only show jobs posted by the logged-in organization
    return render(request, 'jobs/organization_dashboard.html', {'jobs': jobs})

# Create Job (Only accessible to organizations)
@login_required
def job_create(request):
    if request.user.profile.user_type != 'organization':
        messages.error(request, 'You are not authorized to create jobs.')
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('organization_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

# Apply for Job
@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'You have successfully applied for this job!')
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/application_form.html', {'form': form, 'job': job})

@login_required
def dashboard(request):
    # Fetch applications submitted by the logged-in job seeker
    my_applications = Application.objects.filter(applicant=request.user)

    return render(request, 'dashboard.html', {
        'my_applications': my_applications,
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm

# @login_required
# def edit_job(request, pk):
#     # Fetch the job object or return a 404 error if not found
#     job = get_object_or_404(Job, pk=pk)

#     # Ensure only the organizer who posted the job can edit it
#     if job.posted_by != request.user:
#         return redirect('home')  # Redirect unauthorized users

#     if request.method == 'POST':
#         form = JobForm(request.POST, instance=job)
#         if form.is_valid():
#             form.save()
#             return redirect('organization_dashboard')
#     else:
#         form = JobForm(instance=job)

#     return render(request, 'edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, pk):
    # Fetch the job object or return a 404 error if not found
    job = get_object_or_404(Job, pk=pk)

    # Ensure only the organizer who posted the job can delete it
    if job.posted_by != request.user:
        return redirect('home')  # Redirect unauthorized users

    if request.method == 'POST':
        job.delete()
        return redirect('organization_dashboard')

    return render(request, 'delete_job.html', {'job': job})



