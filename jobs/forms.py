from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resume


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["username", "city", "phone",
                  "email", "apply_position", "born_address", "gender",
                  "bachelor_school", "master_school", "major", "degree",
                  "candidate_introduction", "work_experience", "project_experience"]

