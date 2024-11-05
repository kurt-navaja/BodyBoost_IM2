from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import ForgotPasswordForm, ResetPasswordForm
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('notifAll:firstP')
            else:
                logger.error(f"Authentication failed for email: {email}")
                messages.error(request, "Invalid email or password")
                logger.info(f"Error message set: Invalid email or password")
        except User.DoesNotExist:
            logger.error(f"User does not exist for email: {email}")
            messages.error(request, "User with this email does not exist")
            logger.info(f"Error message set: User with this email does not exist")
        
        # Log the messages to see if they're being set
        logger.info(f"Messages after login attempt: {list(messages.get_messages(request))}")
        
        # Store messages in session explicitly
        storage = messages.get_messages(request)
        storage.used = False
        
        # Redirect back to the login page to display the error messages
        return redirect('login:login')

    # If it's a GET request or after a failed POST, check for the error parameter
    error = request.GET.get('error')
    if error:
        messages.error(request, "Login failed. Please try again.")
        logger.info(f"Error message set from GET parameter: Login failed. Please try again.")

    # Log messages before rendering the template
    logger.info(f"Messages before rendering template: {list(messages.get_messages(request))}")

    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    # Logic to handle signup
    return render(request, 'signup.html')

def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            # Store the verified email in session for the next step
            request.session['reset_email'] = email
            messages.success(request, "Email verified. Please enter your new password.")
            logger.info(f"Email verified for password reset: {email}")
            return redirect('login:forgotPassword2')
    
    return render(request, 'forgotPassword.html', {'form': form})

def forgot_password_2_view(request):
    # Get the email from session
    email = request.session.get('reset_email')
    if not email:
        return redirect('login:forgotPassword')
    
    form = ResetPasswordForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                User = get_user_model()
                user = User.objects.get(email=email)
                
                # Set the new password
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                # Clear the session
                del request.session['reset_email']
                
                messages.success(request, "Your password has been successfully reset.")
                logger.info(f"Password successfully reset for user: {email}")
                return redirect('login:forgotPassword3')
                
            except User.DoesNotExist:
                logger.error(f"User not found for email: {email}")
                messages.error(request, "An error occurred. Please try again.")
            except Exception as e:
                logger.error(f"Error resetting password: {str(e)}")
                messages.error(request, "An error occurred while resetting your password.")
    
    return render(request, 'forgotPassword2.html', {'form': form})

def forgot_password_3_view(request):
    # Logic to handle password reset
    return render(request, 'forgotPassword3.html')