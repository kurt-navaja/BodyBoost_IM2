from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from Signup.models import CustomUser  # Import your custom user model
from django.views.decorators.http import require_http_methods


import logging
logger = logging.getLogger(__name__)



def firstP(request):
    return render(request, '1stP.html')

def secondP(request):
    return render(request, '2ndP.html')

@login_required
def accountSettings(request):
    if request.method == 'GET':
        # Render the account settings page
        return render(request, 'accountSettings.html')
    
    if request.method == 'POST':
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            
            weight = request.POST.get('weight')
            if weight:
                try:
                    user.weight = float(weight)
                except ValueError:
                    if is_ajax:
                        return JsonResponse({
                            'status': 'error', 
                            'message': 'Invalid weight format'
                        }, status=400)
                    else:
                        messages.error(request, 'Invalid weight format')
                        return render(request, 'accountSettings.html')
            
            user.body_goal = request.POST.get('body_goal', user.body_goal)
            user.country = request.POST.get('country', user.country)
            user.city = request.POST.get('city', user.city)
            user.street = request.POST.get('street', user.street)
            user.zip_code = request.POST.get('zip', user.zip_code)
            user.intensity = request.POST.get('intensity', user.intensity)
            
            if 'profile_photo' in request.FILES:
                user.profile_photo = request.FILES['profile_photo']
                logger.info(f"Profile photo saved: {user.profile_photo}")
            
            user.save()
            
            logger.info(f"User {user.email} updated successfully.")
            
            # Return appropriate response based on request type
            if is_ajax:
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Account settings updated successfully'
                })
            else:
                messages.success(request, 'Account settings updated successfully')
                return redirect('notifAll:accountSettings')
        
        except Exception as e:
            logger.error(f"Error updating user {user.email}: {str(e)}")
            
            # Return appropriate error response based on request type
            if is_ajax:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Error updating account: {str(e)}'
                }, status=400)
            else:
                messages.error(request, f'Error updating account: {str(e)}')
                return render(request, 'accountSettings.html')
    
    # If somehow method is neither GET nor POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def workout(request):
    return render(request, 'workout.html')

def save_workout_preferences(request):
    if request.method == 'POST':
        body_type = request.POST.get('bodyType')
        fitness_goal = request.POST.get('fitnessGoal')
        fitness_level = request.POST.get('fitnessLevel')
        workout_style = request.POST.get('workoutStyle')
        health_concerns = request.POST.get('healthConcerns')

        # Save data to the session or database
        request.session['body_type'] = body_type
        request.session['fitness_goal'] = fitness_goal
        request.session['fitness_level'] = fitness_level
        request.session['workout_style'] = workout_style
        request.session['health_concerns'] = health_concerns

        # Redirect based on the workout style selected
        if workout_style == 'strength-training':
            return redirect('fitness:strength')
        elif workout_style == 'cardio':
            return redirect('cardio_page')
        elif workout_style == 'flexibility-yoga':
            return redirect('flexibility_yoga_page')

    return HttpResponse("Form submission error")

def login(request):
    return render(request, 'login.html')

def settings(request):
    return render(request, 'settings.html')