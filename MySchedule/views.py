from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import WorkoutPlan, WorkoutType
from Signup.models import CustomUser

def get_personalized_workouts(user):
    # Map intensity to difficulty levels
    intensity_to_difficulty = {
        '0.3': ['Light'],
        '0.6': ['Light', 'Moderate'],
        '0.7': ['Moderate'],
        '0.8': ['Moderate', 'High'],
        '0.9': ['High', 'Extreme']
    }
    
    difficulty_levels = intensity_to_difficulty.get(user.intensity, ['Moderate'])

    personalized_workouts = WorkoutPlan.objects.filter(
        recommended_weight_range_min__lte=user.weight,
        recommended_weight_range_max__gte=user.weight,
        body_goal=user.body_goal,
        gender=user.gender,
        workout_type__difficulty_level__in=difficulty_levels
    ).order_by('?')[:4]  # Randomly select 4 workouts
    
    return personalized_workouts

def my_schedule(request):
    user = request.user
    personalized_workouts = get_personalized_workouts(user)
    
    context = {
        'personalized_workouts': personalized_workouts
    }
    return render(request, 'my_schedule.html', context)

def initialize_workouts_for_user(user):
    """
    Create initial workout plans for a user based on their body goal, 
    weight, and gender.
    """
    # Define workout types for each body goal
    workout_mappings = {
        'victoria-secret-thin': [
            {
                'name': 'Cardio Burn',
                'target_muscles': 'Full Body',
                'difficulty_level': 'Moderate',
                'duration': 45,
                'calories_burned': 350,
                'weight_range_min': 45,
                'weight_range_max': 65
            },
            {
                'name': 'High-Intensity Interval Training',
                'target_muscles': 'Full Body',
                'difficulty_level': 'High',
                'duration': 30,
                'calories_burned': 400,
                'weight_range_min': 45,
                'weight_range_max': 65
            }
        ],
        'slim': [
            {
                'name': 'Lean Muscle Building',
                'target_muscles': 'Core and Legs',
                'difficulty_level': 'Moderate',
                'duration': 60,
                'calories_burned': 400,
                'weight_range_min': 55,
                'weight_range_max': 75
            },
            {
                'name': 'Endurance Training',
                'target_muscles': 'Cardiovascular',
                'difficulty_level': 'Light',
                'duration': 45,
                'calories_burned': 300,
                'weight_range_min': 55,
                'weight_range_max': 75
            }
        ],
        'muscular': [
            {
                'name': 'Strength Training',
                'target_muscles': 'Full Body',
                'difficulty_level': 'High',
                'duration': 75,
                'calories_burned': 500,
                'weight_range_min': 70,
                'weight_range_max': 90
            },
            {
                'name': 'Power Lifting',
                'target_muscles': 'Upper Body',
                'difficulty_level': 'Extreme',
                'duration': 60,
                'calories_burned': 450,
                'weight_range_min': 70,
                'weight_range_max': 90
            }
        ],
        'athletic': [
            {
                'name': 'Cross-Training',
                'target_muscles': 'Full Body',
                'difficulty_level': 'High',
                'duration': 60,
                'calories_burned': 450,
                'weight_range_min': 60,
                'weight_range_max': 80
            },
            {
                'name': 'Functional Fitness',
                'target_muscles': 'Functional Muscles',
                'difficulty_level': 'Moderate',
                'duration': 45,
                'calories_burned': 350,
                'weight_range_min': 60,
                'weight_range_max': 80
            }
        ],
        'sumo-wrestler': [
            {
                'name': 'Heavy Resistance Training',
                'target_muscles': 'Full Body',
                'difficulty_level': 'Extreme',
                'duration': 90,
                'calories_burned': 600,
                'weight_range_min': 90,
                'weight_range_max': 150
            },
            {
                'name': 'Mass Building',
                'target_muscles': 'Upper Body and Core',
                'difficulty_level': 'High',
                'duration': 75,
                'calories_burned': 550,
                'weight_range_min': 90,
                'weight_range_max': 150
            }
        ]
    }

    # Get the workout types for the user's body goal
    goal_workouts = workout_mappings.get(user.body_goal, [])

    # Create WorkoutPlan instances
    for workout_info in goal_workouts:
        # Find or create the corresponding WorkoutType
        workout_type, created = WorkoutType.objects.get_or_create(
            name=workout_info['name'],
            defaults={
                'target_muscles': workout_info['target_muscles'],
                'difficulty_level': workout_info['difficulty_level']
            }
        )

        # Create WorkoutPlan for the user
        WorkoutPlan.objects.create(
            user=user,
            workout_type=workout_type,
            duration=workout_info['duration'],
            calories_burned=workout_info['calories_burned'],
            recommended_weight_range_min=workout_info['weight_range_min'],
            recommended_weight_range_max=workout_info['weight_range_max'],
            body_goal=user.body_goal,
            gender=user.gender
        )
        
# Example usage in a view or signal
def create_initial_workouts(sender, instance, created, **kwargs):
    if created:
        initialize_workouts_for_user(instance)

def mySched(request):
    return render(request, 'mySchedule.html')

