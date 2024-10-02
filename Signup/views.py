from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    # Logic to handle login
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def password_reset_view(request):
    # Logic to handle password reset
    return render(request, 'password_reset.html')

def authentication_view(request):
    return render(request, 'authentication.html')

def authenticationSuccess_view(request):
    return render(request, 'authenticationSuccess.html')

def knowMore_view(request):
    return render(request, 'knowMore.html')