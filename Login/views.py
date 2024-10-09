from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    # Logic to handle signup
    return render(request, 'signup.html')

def forgot_password_view(request):
    # Logic to handle password reset
    return render(request, 'forgotPassword.html')