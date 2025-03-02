from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .forms import RegisterForm, CustomLoginForm

# Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.user_type = form.cleaned_data['user_type']
            user.profile.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(username=username, password=password)

            # Check if the user exists and matches the selected role
            if user is not None and user.profile.user_type == user_type:
                login(request, user)
                if user_type == 'organization':
                    return redirect('organization_dashboard')  # Redirect to organization dashboard
                elif user_type == 'job_seeker':
                    return redirect('job_list')  # Redirect to job list
            else:
                messages.error(request, 'Invalid credentials or role mismatch.')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')