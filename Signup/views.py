from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from .forms import CustomUserCreationForm, KnowMoreForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            return redirect('signup:authenticationSuccess')
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

@login_required
def knowMore_view(request):
    User = get_user_model()
    
    try:
        # Attempt to get the existing user profile
        user_profile = User.objects.get(pk=request.user.pk)
        logger.info(f"Existing user profile found for user {request.user.email}")
    except User.DoesNotExist:
        # If the profile doesn't exist, create a new one
        user_profile = User(email=request.user.email)
        logger.info(f"Creating new user profile for user {request.user.email}")

    if request.method == 'POST':
        form = KnowMoreForm(request.POST, instance=user_profile)
        if form.is_valid():
            user = form.save()
            logger.info(f"Additional information saved for user {user.email}")
            messages.success(request, 'Profile updated successfully!')
            return redirect('signup:knowMoreSuccess')
        else:
            logger.error(f"KnowMore form validation failed. Errors: {form.errors}")
            return render(request, 'knowMore.html', {'form': form})
    else:
        form = KnowMoreForm(instance=user_profile)
    
    return render(request, 'knowMore.html', {'form': form})

def knowMoreSuccess_view(request):
    return render(request, 'knowMoreSuccess.html')