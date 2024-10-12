from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        logger.info(f"POST data received: {request.POST}")
        if form.is_valid():
            user = form.save()
            logger.info(f"User {user.email} saved to the database.")
            login(request, user)
            return redirect('authenticationSuccess')
        else:
            logger.error(f"Form validation failed. Errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def password_reset_view(request):
    # Implement password reset logic here
    return render(request, 'password_reset.html')

def authentication_view(request):
    return render(request, 'authentication.html')

def authenticationSuccess_view(request):
    return render(request, 'authenticationSuccess.html')

def knowMore_view(request):
    return render(request, 'knowMore.html')