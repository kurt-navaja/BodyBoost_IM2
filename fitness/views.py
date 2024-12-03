from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Exercise

def strength(request):
    return render(request, 'strength_beginner.html')

def strength2(request):
    return render(request, 'strength_beginner2.html')

def cardio(request):
    return render(request, 'cardio.html')

def strength_intermediate(request):
    return render(request, 'strength_intermediate.html')

def strength_intermediate2(request):
    return render(request, 'strength_intermediate2.html')

def strength_advanced(request):
    return render(request, 'strength_advanced.html')

def strength_advanced2(request):
    return render(request, 'strength_advanced2.html')

@login_required
def exercise_library(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Filter exercises based on user preferences
    recommended_exercises = Exercise.objects.filter(
        category=user_profile.preferred_style
    )
    
    context = {
        'strength_exercises': Exercise.objects.filter(category='strength_beginner'),
        'cardio_exercises': Exercise.objects.filter(category='cardio'),
        'flexibility_exercises': Exercise.objects.filter(category='flexibility'),
        'recommended_exercises': recommended_exercises,
    }
    return render(request, 'fitness/exercise_library.html', context)