from django.db.models.signals import post_save
from django.dispatch import receiver
from Signup.models import CustomUser
from .models import WorkoutPlan, WorkoutType

@receiver(post_save, sender=CustomUser)
def create_user_workouts(sender, instance, created, **kwargs):
    # Check if user already has workouts to prevent duplicates
    existing_workouts = WorkoutPlan.objects.filter(user=instance)
    
    if created and not existing_workouts.exists():
        initialize_workouts_for_user(instance)

def get_difficulty_level(user_intensity, default_difficulty):
    """
    Map user intensity to workout difficulty
    """
    intensity_difficulty_map = {
        'Gentle': 'Light',
        'Light': 'Light',
        'Moderate': 'Moderate',
        'Aggressive': 'High',
        'High Intensity': 'Extreme'
    }
    
    return intensity_difficulty_map.get(user_intensity, default_difficulty)

def initialize_workouts_for_user(user):
    """
    Create initial workout plans for a user based on their body goal, 
    weight, and intensity.
    """
    # Workout mappings
    workout_mappings = {
        'victoria-secret-thin': [
            {
                'name': 'Cardio Burn',
                'target_muscles': 'Full Body',
                'difficulty_level': get_difficulty_level(user.intensity, 'Light'),
                'duration': 45,
                'calories_burned': 350,
                'weight_range_min': 45,
                'weight_range_max': 65
            },
            {
                'name': 'High-Intensity Interval Training',
                'target_muscles': 'Full Body',
                'difficulty_level': get_difficulty_level(user.intensity, 'High'),
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
                'difficulty_level': get_difficulty_level(user.intensity, 'Moderate'),
                'duration': 60,
                'calories_burned': 400,
                'weight_range_min': 55,
                'weight_range_max': 75
            }
        ],
        'muscular': [
            {
                'name': 'Strength Training',
                'target_muscles': 'Full Body',
                'difficulty_level': get_difficulty_level(user.intensity, 'High'),
                'duration': 75,
                'calories_burned': 500,
                'weight_range_min': 70,
                'weight_range_max': 90
            }
        ],
        'athletic': [
            {
                'name': 'Cross-Training',
                'target_muscles': 'Full Body',
                'difficulty_level': get_difficulty_level(user.intensity, 'High'),
                'duration': 60,
                'calories_burned': 450,
                'weight_range_min': 60,
                'weight_range_max': 80
            }
        ],
        'sumo-wrestler': [
            {
                'name': 'Heavy Resistance Training',
                'target_muscles': 'Full Body',
                'difficulty_level': get_difficulty_level(user.intensity, 'Extreme'),
                'duration': 90,
                'calories_burned': 600,
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
        
        print(f"User body goal: {user.body_goal}")
    print(f"User intensity: {user.intensity}")
    goal_workouts = workout_mappings.get(user.body_goal, [])
    print(f"Goal workouts: {goal_workouts}")
    
    if not goal_workouts:
        print("No workouts found for this body goal!")