from django.shortcuts import render
from .models import WorkoutPlan
from .signals import initialize_workouts_for_user

def get_personalized_workouts(user):
    # Ensure workouts exist for the user
    user_workouts = WorkoutPlan.objects.filter(user=user)
    
    if not user_workouts.exists():
        # If no workouts exist, create them
        initialize_workouts_for_user(user)
        user_workouts = WorkoutPlan.objects.filter(user=user)
    
    # Map intensity to difficulty levels
    intensity_to_difficulty = {
        'Gentle': ['Light'],
        'Light': ['Light', 'Moderate'],
        'Moderate': ['Moderate'],
        'Aggressive': ['Moderate', 'High'],
        'High Intensity': ['High', 'Extreme']
    }
    
    difficulty_levels = intensity_to_difficulty.get(user.intensity, ['Moderate'])

    # Filter workouts based on user's body goal and intensity
    personalized_workouts = user_workouts.filter(
        body_goal=user.body_goal,
        workout_type__difficulty_level__in=difficulty_levels
    ).order_by('?')[:4]  # Randomly select 4 workouts
    
    return personalized_workouts

def mySched(request):
    user = request.user
    personalized_workouts = get_personalized_workouts(user)
    
    context = {
        'personalized_workouts': personalized_workouts
    }
    return render(request, 'mySchedule.html', context)
