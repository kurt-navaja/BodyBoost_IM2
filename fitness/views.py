from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Exercise

def strength(request):
    return render(request, 'strength.html')


@login_required
def exercise_library(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    # Filter exercises based on user preferences
    recommended_exercises = Exercise.objects.filter(
        category=user_profile.preferred_style
    )
    
    context = {
        'strength_exercises': Exercise.objects.filter(category='strength'),
        'cardio_exercises': Exercise.objects.filter(category='cardio'),
        'flexibility_exercises': Exercise.objects.filter(category='flexibility'),
        'recommended_exercises': recommended_exercises,
    }
    return render(request, 'fitness/exercise_library.html', context)