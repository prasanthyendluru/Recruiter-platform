from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    USER_TYPE_CHOICES = (
        ('organization', 'Organization'),
        ('job_seeker', 'Job Seeker'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class CustomLoginForm(AuthenticationForm):
    USER_TYPE_CHOICES = (
        ('organization', 'Organization'),
        ('job_seeker', 'Job Seeker'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)