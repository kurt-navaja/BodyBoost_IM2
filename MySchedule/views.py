from django.shortcuts import render # type: ignore
from django.utils import timezone # type: ignore
from django.db import transaction # type: ignore
from .models import WorkoutPlan, WorkoutSelectionLog
from .signals import initialize_workouts_for_user
import json

def get_personalized_workouts(user):
    
    # Extensive logging
    print("--- Detailed Workout Selection Debug ---")
    print(f"User: {user.first_name}")
    print(f"Body Goal: {user.body_goal}")
    print(f"Intensity: {user.intensity}")
    
    # Ensure we always have workouts
    user_workouts = WorkoutPlan.objects.filter(
        user=user, 
        body_goal=user.body_goal.lower()
    )
    
    # If no workouts exist for current body goal, recreate
    if not user_workouts.exists():
        print("No workouts found for current body goal. Recreating...")
        initialize_workouts_for_user(user)
        user_workouts = WorkoutPlan.objects.filter(
            user=user, 
            body_goal=user.body_goal.lower()
        )
    
    print(f"Total User Workouts: {user_workouts.count()}")
    print("Existing Workout Details:")
    for workout in user_workouts:
        print(f"- {workout.workout_type.name} | Difficulty: {workout.workout_type.difficulty_level} | Body Goal: {workout.body_goal}")

    # Intensity to difficulty mapping with more flexibility
    intensity_to_difficulty = {
        'Gentle': ['Light'],
        'Light': ['Light', 'Light', 'Light', 'Moderate'],
        'Moderate': ['Light', 'Moderate', 'Moderate', 'Moderate'],
        'Aggressive': ['Moderate', 'High', 'High', 'High'],
        'High Intensity': ['Moderate', 'High', 'Extreme', 'Extreme'],
    }
    
    difficulty_levels = intensity_to_difficulty.get(user.intensity, ['Moderate'])
    print(f"Mapped Difficulty Levels: {difficulty_levels}")

    # Filter workouts with more logging
    filtered_workouts = user_workouts.filter(
        body_goal=user.body_goal.lower(),
        workout_type__difficulty_level__in=difficulty_levels
    )
    
    print(f"Filtered Workouts Count: {filtered_workouts.count()}")
    if not filtered_workouts.exists():
        print("WARNING: No workouts match the current filters!")
        print(f"Checked conditions:")
        print(f"- Body Goal: {user.body_goal}")
        print(f"- Difficulty Levels: {difficulty_levels}")
        
    # Try to get existing log or create a new one
    try:
        last_selection = WorkoutSelectionLog.objects.get(user=user)
    except WorkoutSelectionLog.DoesNotExist:
        last_selection = None

    # Conditions to regenerate workouts
    regenerate_workouts = (
        not last_selection or 
        last_selection.date.date() != timezone.now().date() or
        last_selection.user_intensity != user.intensity or 
        last_selection.body_goal != user.body_goal
    )

    with transaction.atomic():
        if regenerate_workouts:
            # Logging to confirm regeneration
            print(f"REGENERATING WORKOUTS - Reason:")
            if not last_selection:
                print("- No previous selection log")
            elif last_selection.date.date() != timezone.now().date():
                print("- Different date")
            elif last_selection.user_intensity != user.intensity:
                print("- Intensity changed")
            elif last_selection.body_goal != user.body_goal:
                print("- Body goal changed")

            # Filter workouts by body goal and mapped difficulty levels
            personalized_workouts = user_workouts.filter(
                body_goal=user.body_goal.lower(),
                workout_type__difficulty_level__in=difficulty_levels
            ).order_by('?')[:5]

            if not personalized_workouts.exists():
                print("WARNING: No workouts match new difficulty. Falling back to original workouts.")
                personalized_workouts = user_workouts.filter(body_goal=user.body_goal.lower())[:5]

            # Create or update the selection log
            selection_log, created = WorkoutSelectionLog.objects.update_or_create(
                user=user,
                defaults={
                    'date': timezone.now(),
                    'user_intensity': user.intensity,
                    'body_goal': user.body_goal
                }
            )
            
            # Set and save selected workout IDs
            selection_log.set_selected_workouts(list(personalized_workouts.values_list('id', flat=True)))
            selection_log.save()
        else:
            # Retrieve previously selected workouts
            last_selected_workout_ids = last_selection.get_selected_workouts()
            personalized_workouts = WorkoutPlan.objects.filter(id__in=last_selected_workout_ids)
    
    return personalized_workouts

def mySched(request):
    user = request.user
    personalized_workouts = get_personalized_workouts(user)
    
    context = {
        'personalized_workouts': personalized_workouts
    }
    return render(request, 'mySchedule.html', context)
