from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Exercise

def strength(request):
    return render(request, 'Strength/strength_beginner.html')

def strength2(request):
    return render(request, 'Strength/strength_beginner2.html')

def strength_progress(request):
    return render(request, 'Strength/strength_beginner_progress.html')

def strength_intermediate(request):
    return render(request, 'Strength/strength_intermediate.html')

def strength_intermediate2(request):
    return render(request, 'Strength/strength_intermediate2.html')

def strength_intermediate_progress(request):
    return render(request, 'Strength/strength_intermediate_progress.html')

def strength_advanced(request):
    return render(request, 'Strength/strength_advanced.html')

def strength_advanced2(request):
    return render(request, 'Strength/strength_advanced2.html')

def strength_advanced_progress(request):
    return render(request, 'Strength/strength_advanced_progress.html')

def cardio_beginner(request):
    return render(request, 'Cardio/cardio_beginner.html')

def cardio_beginner2(request):
    return render(request, 'Cardio/cardio_beginner2.html')

def cardio_beginner_progress(request):
    return render(request, 'Cardio/cardio_beginner_progress.html')

def cardio_intermediate(request):
    return render(request, 'Cardio/cardio_intermediate.html')

def cardio_intermediate2(request):
    return render(request, 'Cardio/cardio_intermediate2.html')

def cardio_intermediate_progress(request):
    return render(request, 'Cardio/cardio_intermediate_progress.html')

def cardio_advanced(request):
    return render(request, 'Cardio/cardio_advanced.html')

def cardio_advanced2(request):
    return render(request, 'Cardio/cardio_advanced2.html')

def cardio_advanced_progress(request):
    return render(request, 'Cardio/cardio_advanced_progress.html')

def yoga_beginner(request):
    return render(request, 'Yoga/yoga_beginner.html')

def yoga_beginner2(request):
    return render(request, 'Yoga/yoga_beginner2.html')

def yoga_beginner_progress(request):
    return render(request, 'Yoga/yoga_beginner_progress.html')

def yoga_intermediate(request):
    return render(request, 'Yoga/yoga_intermediate.html')

def yoga_intermediate2(request):
    return render(request, 'Yoga/yoga_intermediate2.html')

def yoga_intermediate_progress(request):
    return render(request, 'Yoga/yoga_intermediate_progress.html')

def yoga_advanced(request):
    return render(request, 'Yoga/yoga_advanced.html')

def yoga_advanced2(request):
    return render(request, 'Yoga/yoga_advanced2.html')

def yoga_advanced_progress(request):
    return render(request, 'Yoga/yoga_advanced_progress.html')


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