from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def firstP(request):
    return render(request, '1stP.html')

# def secondP(request):
#     return render(request, '2ndP.html')

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

        # Redirect based on the workout style and fitness level selected
        if workout_style == 'strength-training':
            if fitness_level == 'beginner':
                return redirect('fitness:strength_beginner')
            elif fitness_level == 'intermediate':
                return redirect('fitness:strength_intermediate')
            elif fitness_level == 'advanced':
                return redirect('fitness:strength_advanced')
        elif workout_style == 'cardio':
            if fitness_level == 'beginner':
                return redirect('fitness:cardio_beginner')
            elif fitness_level == 'intermediate':
                return redirect('fitness:cardio_intermediate')
            elif fitness_level == 'advanced':
                return redirect('fitness:cardio_advanced')
        elif workout_style == 'flexibility-yoga':
            if fitness_level == 'beginner':
                return redirect('flexibility_yoga_beginner')
            elif fitness_level == 'intermediate':
                return redirect('flexibility_yoga_intermediate')
            elif fitness_level == 'advanced':
                return redirect('flexibility_yoga_advanced')

    return HttpResponse("Form submission error")

def login(request):
    return render(request, 'login.html')

def settings(request):
    return redirect('notifAll:accountSettings')

# @login_required
# def homepage_view(request):
#     user = request.user
#     homepage_settings = user.homepage_settings  # Access related HomepageSettings

#     return render(request, 'homepage.html', {'user': user, 'homepage_settings': homepage_settings})