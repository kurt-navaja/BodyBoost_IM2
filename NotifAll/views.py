from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def firstP(request):
    return render(request, '1stP.html')

def secondP(request):
    return render(request, '2ndP.html')

def accountSettings(request):
    return render(request, 'accountSettings.html')

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

# @login_required
# def homepage_view(request):
#     user = request.user
#     homepage_settings = user.homepage_settings  # Access related HomepageSettings

#     return render(request, 'homepage.html', {'user': user, 'homepage_settings': homepage_settings})