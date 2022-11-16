from django.urls import path
from jobs import views

urlpatterns = [
    path('job/<int:job_id>/', views.detail, name='detail'),
    path("joblist/", views.joblist, name="joblist"),
    path("home/", views.joblist, name="joblist"),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('new-resume/', views.resume_new, name='resume_new'),
    path('resumes/<int:resume_id>/', views.resume_detail, name='resume_detail'),
]
