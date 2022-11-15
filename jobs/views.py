from django.shortcuts import render, redirect
from django.http import Http404
from jobs.models import Job, Cities, JobTypes
from .forms import RegisterForm, ResumeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def joblist(request):
    job_list = Job.objects.order_by("job_type")
    context = {"job_list": job_list}

    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]

    return render(request, 'jobs/joblist.html', context)


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404("Job does not exist")
    return render(request, 'jobs/job.html', {'job': job})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def new_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.applicant = request.user
            resume.save()
            return redirect("/home")
    else:
        form = ResumeForm()

    return render(request, 'jobs/new_resume.html', {"form": form})