from django.db.models.signals import post_save # type: ignore
from django.dispatch import receiver # type: ignore
from django.db import transaction # type: ignore
from Signup.models import CustomUser
from .models import WorkoutPlan, WorkoutType, WorkoutSelectionLog, MealPlan, MealSelectionLog, MealType

@receiver(post_save, sender=CustomUser)
def create_user_workouts(sender, instance, created, **kwargs):
    print(f"Signal Details:")
    print(f"User: {instance.first_name}")
    print(f"Created flag: {created}")
    print(f"Body Goal: {instance.body_goal}")
    print(f"Intensity: {instance.intensity}")
    
    # Always remove existing workouts and create new ones
    with transaction.atomic():
        # Delete existing workout plans for this user
        WorkoutPlan.objects.filter(user=instance).delete()
        
        # Delete any existing workout selection logs
        WorkoutSelectionLog.objects.filter(user=instance).delete()
        
        # Initialize new workouts
        print("Initializing NEW workouts for user...")
        initialize_workouts_for_user(instance)
    
    # Check if user has no workouts, regardless of created flag
    existing_workouts = WorkoutPlan.objects.filter(user=instance)
    
    print(f"Existing workouts count: {existing_workouts.count()}")
    print(f"Body Goal: {instance.body_goal}")
    print(f"Intensity: {instance.intensity}")
    
    # Create workouts if no workouts exist
    if existing_workouts.count() == 0:
        print("Initializing workouts for user...")
        initialize_workouts_for_user(instance)
    else:
        print("Workouts already exist for this user.")

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
        # Light Intensity Workouts
        {
            'name': 'Yoga Flow',
            'target_muscles': 'Flexibility and Relaxation',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 180,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Pilates Core Stretch',
            'target_muscles': 'Core and Flexibility',
            'difficulty_level': 'Light',
            'duration': 30,
            'calories_burned': 200,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Low-Impact Dance',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 160,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Plank Hold',
            'target_muscles': 'Core',
            'difficulty_level': 'Light',
            'duration': 10,
            'calories_burned': 80,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Slow Walk',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        
        # Moderate Intensity Workouts
        {
            'name': 'Barre Sculpt',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'Moderate',
            'duration': 30,
            'calories_burned': 280,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Resistance Band Training',
            'target_muscles': 'Arms and Legs',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Active Stretching',
            'target_muscles': 'Flexibility and Core',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 170,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Pilates Reformer',
            'target_muscles': 'Core and Legs',
            'difficulty_level': 'Moderate',
            'duration': 30,
            'calories_burned': 320,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Bodyweight Circuit',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 270,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        
        # High Intensity Workouts
        {
            'name': 'HIIT (High-Intensity Interval Training)',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 420,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Speed Jump Rope',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'High',
            'duration': 10,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Mountain Climbers',
            'target_muscles': 'Core and Cardio',
            'difficulty_level': 'High',
            'duration': 15,
            'calories_burned': 260,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Dynamic Plank Series',
            'target_muscles': 'Core and Arms',
            'difficulty_level': 'High',
            'duration': 10,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Power Yoga',
            'target_muscles': 'Core and Flexibility',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 360,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        
        # Extreme Intensity Workouts
        {
            'name': 'Tabata Cardio',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 310,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Burpee Blast',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 260,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Sprint Intervals',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'Extreme',
            'duration': 15,
            'calories_burned': 420,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Plank Jacks',
            'target_muscles': 'Core and Legs',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 210,
            'weight_range_min': 45,
            'weight_range_max': 65
        },
        {
            'name': 'Explosive Lunges',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 270,
            'weight_range_min': 45,
            'weight_range_max': 65
        }
        ],       
        'slim': [
        # Light Intensity Workouts
        {
            'name': 'Yoga Flow',
            'target_muscles': 'Flexibility and Relaxation',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 170,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Pilates Core Stretch',
            'target_muscles': 'Core and Flexibility',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 190,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Plank Hold',
            'target_muscles': 'Core',
            'difficulty_level': 'Light',
            'duration': 10,
            'calories_burned': 70,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Slow Walk',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Light',
            'duration': 40,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Gentle Stretching',
            'target_muscles': 'Flexibility and Core',
            'difficulty_level': 'Light',
            'duration': 10,
            'calories_burned': 120,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        
        # Moderate Intensity Workouts
        {
            'name': 'Barre Sculpt',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 270,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Bodyweight Circuit',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 280,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Resistance Band Training',
            'target_muscles': 'Arms and Legs',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 230,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Active Stretching',
            'target_muscles': 'Flexibility and Core',
            'difficulty_level': 'Moderate',
            'duration': 10,
            'calories_burned': 180,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Low Impact Cardio',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 240,
            'weight_range_min': 45,
            'weight_range_max': 75
        },

        # High Intensity Workouts
        {
            'name': 'HIIT (High-Intensity Interval Training)',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 420,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Speed Jump Rope',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'High',
            'duration': 15,
            'calories_burned': 230,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Mountain Climbers',
            'target_muscles': 'Core and Cardio',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 260,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Dynamic Plank Series',
            'target_muscles': 'Core and Arms',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Power Yoga',
            'target_muscles': 'Core and Flexibility',
            'difficulty_level': 'High',
            'duration': 30,
            'calories_burned': 360,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        
        # Extreme Intensity Workouts
        {
            'name': 'Tabata Cardio',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 320,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Burpee Blast',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 270,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Sprint Intervals',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 410,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Plank Jacks',
            'target_muscles': 'Core and Legs',
            'difficulty_level': 'Extreme',
            'duration': 15,
            'calories_burned': 220,
            'weight_range_min': 45,
            'weight_range_max': 75
        },
        {
            'name': 'Explosive Lunges',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 260,
            'weight_range_min': 45,
            'weight_range_max': 75
        }
        ],
        'muscular': [
        # Light Intensity Workouts
        {
            'name': 'Active Stretching for Strength',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 120,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Yoga for Muscle Recovery',
            'target_muscles': 'Flexibility and Core',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 140,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Resistance Band Recovery',
            'target_muscles': 'Arms and Legs',
            'difficulty_level': 'Light',
            'duration': 25,
            'calories_burned': 170,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Foam Rolling for Hypertrophy',
            'target_muscles': 'Legs and Back',
            'difficulty_level': 'Light',
            'duration': 15,
            'calories_burned': 70,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Core Stability Drills',
            'target_muscles': 'Core and Lower Back',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 120,
            'weight_range_min': 70,
            'weight_range_max': 90
        },

        # Moderate Intensity Workouts
        {
            'name': 'Hypertrophy Circuit',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 30,
            'calories_burned': 360,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Dumbbell Strength Training',
            'target_muscles': 'Arms and Shoulders',
            'difficulty_level': 'Moderate',
            'duration': 35,
            'calories_burned': 270,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Push-Pull Superset',
            'target_muscles': 'Chest and Back',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 330,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Leg Day Essentials',
            'target_muscles': 'Legs and Glutes',
            'difficulty_level': 'Moderate',
            'duration': 25,
            'calories_burned': 400,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Barbell Complex',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 350,
            'weight_range_min': 70,
            'weight_range_max': 90
        },

        # High Intensity Workouts
        {
            'name': 'Weighted HIIT',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 400,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Explosive Power Training',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'High',
            'duration': 10,
            'calories_burned': 350,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Heavy Compound Lifts',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 450,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Plyometric Box Jumps',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'High',
            'duration': 10,
            'calories_burned': 250,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Kettlebell Swings',
            'target_muscles': 'Glutes and Core',
            'difficulty_level': 'High',
            'duration': 15,
            'calories_burned': 300,
            'weight_range_min': 70,
            'weight_range_max': 90
        },

        # Extreme Intensity Workouts
        {
            'name': 'Powerlifting Max Effort',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 500,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Drop Set Challenge',
            'target_muscles': 'Arms and Shoulders',
            'difficulty_level': 'Extreme',
            'duration': 15,
            'calories_burned': 400,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Battle Rope Endurance',
            'target_muscles': 'Arms and Core',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 300,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Explosive Deadlifts',
            'target_muscles': 'Back and Legs',
            'difficulty_level': 'Extreme',
            'duration': 10,
            'calories_burned': 400,
            'weight_range_min': 70,
            'weight_range_max': 90
        },
        {
            'name': 'Extreme CrossFit Circuit',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 30,
            'calories_burned': 600,
            'weight_range_min': 70,
            'weight_range_max': 90
        }
        ],
        'athletic': [
        # Light Intensity Workouts
        {
            'name': 'Yoga for Athletes',
            'target_muscles': 'Flexibility and Core',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 150,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Dynamic Stretching',
            'target_muscles': 'Flexibility and Mobility',
            'difficulty_level': 'Light',
            'duration': 10,
            'calories_burned': 100,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Active Recovery Walk',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 180,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Foam Rolling Session',
            'target_muscles': 'Flexibility and Recovery',
            'difficulty_level': 'Light',
            'duration': 10,
            'calories_burned': 50,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Balance and Stability Drills',
            'target_muscles': 'Core and Legs',
            'difficulty_level': 'Light',
            'duration': 15,
            'calories_burned': 120,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        
        # Moderate Intensity Workouts
        {
            'name': 'Strength Endurance Circuit',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 300,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Core Stability Training',
            'target_muscles': 'Core and Back',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 200,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Agility Ladder Drills',
            'target_muscles': 'Legs and Coordination',
            'difficulty_level': 'Moderate',
            'duration': 15,
            'calories_burned': 200,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Resistance Band Circuit',
            'target_muscles': 'Arms, Legs, and Core',
            'difficulty_level': 'Moderate',
            'duration': 25,
            'calories_burned': 250,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Plyometric Prep',
            'target_muscles': 'Legs and Power',
            'difficulty_level': 'Moderate',
            'duration': 10,
            'calories_burned': 220,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        
        # High Intensity Workouts
        {
            'name': 'HIIT Strength Blast',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 30,
            'calories_burned': 400,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Sprint Intervals',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 350,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Power Circuit Training',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 30,
            'calories_burned': 400,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Explosive Box Jumps',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'High',
            'duration': 15,
            'calories_burned': 200,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Dynamic Push-Up Series',
            'target_muscles': 'Arms and Core',
            'difficulty_level': 'High',
            'duration': 15,
            'calories_burned': 250,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        
        # Extreme Intensity Workouts
        {
            'name': 'Tabata Power Drills',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 400,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Weighted Burpee Challenge',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 15,
            'calories_burned': 350,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Battle Rope Blast',
            'target_muscles': 'Arms and Core',
            'difficulty_level': 'Extreme',
            'duration': 15,
            'calories_burned': 300,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Explosive Lunges with Weights',
            'target_muscles': 'Legs and Cardio',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 300,
            'weight_range_min': 60,
            'weight_range_max': 80
        },
        {
            'name': 'Extreme CrossFit WOD',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 25,
            'calories_burned': 500,
            'weight_range_min': 60,
            'weight_range_max': 80
        }
        ],
        'sumo-wrestler': [
        # Light Intensity Workouts
        {
            'name': 'Dynamic Stretching Routine',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Light',
            'duration': 15,
            'calories_burned': 100,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Yoga for Flexibility and Recovery',
            'target_muscles': 'Flexibility and Core',
            'difficulty_level': 'Light',
            'duration': 30,
            'calories_burned': 150,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Resistance Band Stamina Drills',
            'target_muscles': 'Arms and Legs',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 120,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Balance Training',
            'target_muscles': 'Core and Lower Body',
            'difficulty_level': 'Light',
            'duration': 25,
            'calories_burned': 100,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Core Stability and Recovery',
            'target_muscles': 'Core and Lower Back',
            'difficulty_level': 'Light',
            'duration': 20,
            'calories_burned': 110,
            'weight_range_min': 90,
            'weight_range_max': 150
        },

        # Moderate Intensity Workouts
        {
            'name': 'Heavy Bag Training',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 350,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Sumo Deadlifts',
            'target_muscles': 'Legs and Back',
            'difficulty_level': 'Moderate',
            'duration': 25,
            'calories_burned': 400,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Pushing and Pulling Drills',
            'target_muscles': 'Chest and Back',
            'difficulty_level': 'Moderate',
            'duration': 20,
            'calories_burned': 300,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Power Cleans',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Moderate',
            'duration': 25,
            'calories_burned': 400,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Heavy Leg Press',
            'target_muscles': 'Legs and Glutes',
            'difficulty_level': 'Moderate',
            'duration': 15,
            'calories_burned': 300,
            'weight_range_min': 90,
            'weight_range_max': 150
        },

        # High Intensity Workouts
        {
            'name': 'Weighted HIIT Circuit',
            'target_muscles': 'Full Body',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 450,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Explosive Power Slams',
            'target_muscles': 'Arms and Core',
            'difficulty_level': 'High',
            'duration': 25,
            'calories_burned': 350,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Battle Rope Power Training',
            'target_muscles': 'Arms and Shoulders',
            'difficulty_level': 'High',
            'duration': 25,
            'calories_burned': 400,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Explosive Squats',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'High',
            'duration': 20,
            'calories_burned': 300,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Farmer’s Walks',
            'target_muscles': 'Grip and Shoulders',
            'difficulty_level': 'High',
            'duration': 15,
            'calories_burned': 250,
            'weight_range_min': 90,
            'weight_range_max': 150
        },

        # Extreme Intensity Workouts
        {
            'name': 'Heavy Resistance Training',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 50,
            'calories_burned': 600,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Tire Flipping Challenge',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 30,
            'calories_burned': 500,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Max Effort Bench Press',
            'target_muscles': 'Chest and Arms',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 400,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Explosive Clean and Jerks',
            'target_muscles': 'Full Body',
            'difficulty_level': 'Extreme',
            'duration': 25,
            'calories_burned': 550,
            'weight_range_min': 90,
            'weight_range_max': 150
        },
        {
            'name': 'Weighted Sumo Stance Drills',
            'target_muscles': 'Legs and Core',
            'difficulty_level': 'Extreme',
            'duration': 20,
            'calories_burned': 450,
            'weight_range_min': 90,
            'weight_range_max': 150
        }
    ]
    }
    
    print(f"Initializing workouts for user: {user.first_name}")
    print(f"Body Goal: {user.body_goal}")
    print(f"Intensity: {user.intensity}")

    # Normalize body goal to lowercase for consistent matching
    body_goal = user.body_goal.lower()

    # Get workouts for the specific body goal
    goal_workouts = workout_mappings.get(body_goal, [])

    if not goal_workouts:
        print(f"ERROR: No workouts found for body goal: {body_goal}")
        return

    # Determine difficulty level based on user's intensity
    difficulty = get_difficulty_level(user.intensity, 'Moderate')
    
    difficulty_hierarchy = {
        'Light': ['Light', 'Moderate'],
        'Moderate': ['Light', 'Moderate', 'High'],
        'High': ['Moderate', 'High', 'Extreme'],
        'Extreme': ['High', 'Extreme']
    }
    
    # Filter workouts by difficulty
    filtered_workouts = [
        workout for workout in goal_workouts 
        if workout['difficulty_level'].lower() in difficulty_hierarchy.get(difficulty.capitalize(), [difficulty.lower()])
    ]

    if not filtered_workouts:
        # Fallback to all workouts if no workouts match exact difficulty
        filtered_workouts = goal_workouts
        print(f"WARNING: No workouts found for difficulty {difficulty}. Using all workouts.")

    # Ensure at least some workouts are created
    if not filtered_workouts:
        print(f"CRITICAL: No workouts could be created for user {user.first_name}")
        return

    # Create WorkoutPlan instances
    created_workouts = []
    for workout_info in filtered_workouts:
        try:
            # Find or create the corresponding WorkoutType
            workout_type, created = WorkoutType.objects.get_or_create(
                name=workout_info['name'],
                defaults={
                    'target_muscles': workout_info['target_muscles'],
                    'difficulty_level': workout_info['difficulty_level']
                }
            )

            # Create WorkoutPlan for the user
            workout_plan = WorkoutPlan.objects.create(
                user=user,
                workout_type=workout_type,
                duration=workout_info['duration'],
                calories_burned=workout_info['calories_burned'],
                recommended_weight_range_min=workout_info['weight_range_min'],
                recommended_weight_range_max=workout_info['weight_range_max'],
                body_goal=body_goal,
                gender=user.gender
            )
            created_workouts.append(workout_plan)
            print(f"Created workout: {workout_plan}")

        except Exception as e:
            print(f"Error creating workout: {e}")

    if not created_workouts:
        print(f"CRITICAL: No workouts were created for user {user.first_name}")
        
        
        
@receiver(post_save, sender=CustomUser)
def create_user_meals(sender, instance, created, **kwargs):
    with transaction.atomic():
        # Delete existing meal plans
        MealPlan.objects.filter(user=instance).delete()
        MealSelectionLog.objects.filter(user=instance).delete()
        
        # Initialize new meals
        initialize_meals_for_user(instance)
        
def initialize_meals_for_user(user):
    # Meal mappings based on body goals
    meal_mappings = {
        'victoria-secret-thin': [
            {
                'name': 'Poached Eggs with Brocolli and Avocado',
                'category': 'Breakfast',
                'target_nutrients': 'Low Calorie, High Protein',
                'calories_range_min': 250,
                'calories_range_max': 410,
                'proteins': 20,
                'carbs': 30,
                'fats': 8,
                'body_goal': 'victoria-secret-thin'
            },
            {
                'name': 'Green Salad with Grilled Chicken',
                'category': 'Lunch',
                'target_nutrients': 'Low Calorie, Moderate Protein',
                'calories_range_min': 300,
                'calories_range_max': 530,
                'proteins': 29,
                'carbs': 20,
                'fats': 12,
                'body_goal': 'victoria-secret-thin'
            },
            {
                'name': 'Vegetable Stir Fry',
                'category': 'Dinner',
                'target_nutrients': 'Low Calorie, High Fiber',
                'calories_range_min': 300,
                'calories_range_max': 470,
                'proteins': 20,
                'carbs': 25,
                'fats': 10,
                'body_goal': 'victoria-secret-thin'
            },
            {
                'name': 'Greek Yogurt with Berries',
                'category': 'Snacks',
                'target_nutrients': 'Low Calorie, Moderate Protein',
                'calories_range_min': 150,
                'calories_range_max': 260,
                'proteins': 10,
                'carbs': 15,
                'fats': 5,
                'body_goal': 'victoria-secret-thin'
            },
            {
                'name': 'Detox Green Tea',
                'category': 'Drinks',
                'target_nutrients': 'Zero Calorie, Antioxidant',
                'calories_range_min': 0,
                'calories_range_max': 30,
                'proteins': 0,
                'carbs': 0,
                'fats': 0,
                'body_goal': 'victoria-secret-thin'
            },
        ],
        'slim': [
            {
                'name': 'Avocado Toast with Egg',
                'category': 'Breakfast',
                'target_nutrients': 'Moderate Calorie, Balanced',
                'calories_range_min': 300,
                'calories_range_max': 430,
                'proteins': 12,
                'carbs': 40,
                'fats': 15,
                'body_goal': 'slim'
            },
            {
                'name': 'Quinoa Bowl with Veggies',
                'category': 'Lunch',
                'target_nutrients': 'Balanced Calorie, High Fiber',
                'calories_range_min': 400,
                'calories_range_max': 520,
                'proteins': 20,
                'carbs': 50,
                'fats': 15,
                'body_goal': 'slim'
            },
            {
                'name': 'Grilled Salmon with Asparagus',
                'category': 'Dinner',
                'target_nutrients': 'Moderate Calorie, Omega-3 Rich',
                'calories_range_min': 400,
                'calories_range_max': 560,
                'proteins': 35,
                'carbs': 10,
                'fats': 20,
                'body_goal': 'slim'
            },
            {
                'name': 'Nuts and Dried Fruits',
                'category': 'Snacks',
                'target_nutrients': 'Moderate Calorie, Healthy Fats',
                'calories_range_min': 200,
                'calories_range_max': 310,
                'proteins': 6,
                'carbs': 20,
                'fats': 15,
                'body_goal': 'slim'
            },
            {
                'name': 'Smoothie with Almond Milk',
                'category': 'Drinks',
                'target_nutrients': 'Low Calorie, Nutrient-Dense',
                'calories_range_min': 100,
                'calories_range_max': 190,
                'proteins': 5,
                'carbs': 20,
                'fats': 3,
                'body_goal': 'slim'
            },
        ],
                'athletic': [
            {
                'name': 'Oats with Peanut Butter and Banana',
                'category': 'Breakfast',
                'target_nutrients': 'High Calorie, High Protein',
                'calories_range_min': 400,
                'calories_range_max': 600,
                'proteins': 20,
                'carbs': 60,
                'fats': 15,
                'body_goal': 'athletic'
            },
            {
                'name': 'Chicken Caesar Salad Wrap',
                'category': 'Lunch',
                'target_nutrients': 'Balanced Calorie, Protein-Rich',
                'calories_range_min': 450,
                'calories_range_max': 650,
                'proteins': 30,
                'carbs': 35,
                'fats': 15,
                'body_goal': 'athletic'
            },
            {
                'name': 'Grilled Steak with Sweet Potato',
                'category': 'Dinner',
                'target_nutrients': 'High Calorie, High Protein',
                'calories_range_min': 500,
                'calories_range_max': 710,
                'proteins': 40,
                'carbs': 50,
                'fats': 20,
                'body_goal': 'athletic'
            },
            {
                'name': 'Protein Bar',
                'category': 'Snacks',
                'target_nutrients': 'Moderate Calorie, High Protein',
                'calories_range_min': 200,
                'calories_range_max': 360,
                'proteins': 20,
                'carbs': 25,
                'fats': 8,
                'body_goal': 'athletic'
            },
            {
                'name': 'Electrolyte Sports Drink',
                'category': 'Drinks',
                'target_nutrients': 'Low Calorie, Electrolyte-Rich',
                'calories_range_min': 50,
                'calories_range_max': 130,
                'proteins': 0,
                'carbs': 20,
                'fats': 0,
                'body_goal': 'athletic'
            },
        ],
                'muscular': [
            {
                'name': 'Egg White Omelette with Whole Grain Toast',
                'category': 'Breakfast',
                'target_nutrients': 'High Protein, Moderate Carb',
                'calories_range_min': 500,
                'calories_range_max': 660,
                'proteins': 35,
                'carbs': 45,
                'fats': 10,
                'body_goal': 'muscular'
            },
            {
                'name': 'Grilled Chicken Breast with Brown Rice and Broccoli',
                'category': 'Lunch',
                'target_nutrients': 'High Calorie, High Protein',
                'calories_range_min': 550,
                'calories_range_max': 710,
                'proteins': 50,
                'carbs': 60,
                'fats': 15,
                'body_goal': 'muscular'
            },
            {
                'name': 'Beef Stir Fry with Quinoa',
                'category': 'Dinner',
                'target_nutrients': 'High Calorie, Balanced',
                'calories_range_min': 600,
                'calories_range_max': 770,
                'proteins': 45,
                'carbs': 50,
                'fats': 20,
                'body_goal': 'muscular'
            },
            {
                'name': 'Cottage Cheese and Fruit',
                'category': 'Snacks',
                'target_nutrients': 'Moderate Calorie, High Protein',
                'calories_range_min': 200,
                'calories_range_max': 390,
                'proteins': 20,
                'carbs': 15,
                'fats': 5,
                'body_goal': 'muscular'
            },
            {
                'name': 'Post-Workout Protein Shake',
                'category': 'Drinks',
                'target_nutrients': 'High Protein, Low Fat',
                'calories_range_min': 150,
                'calories_range_max': 580,
                'proteins': 30,
                'carbs': 15,
                'fats': 2,
                'body_goal': 'muscular'
            },
        ],
                'sumo-wrestler': [
            {
                'name': 'Full Japanese Breakfast',
                'category': 'Breakfast',
                'target_nutrients': 'High Calorie, Balanced Nutrients',
                'calories_range_min': 800,
                'calories_range_max': 900,
                'proteins': 40,
                'carbs': 100,
                'fats': 30,
                'body_goal': 'sumo-wrestler'
            },
            {
                'name': 'Rice Bowl with Pork Belly and Pickled Vegetables',
                'category': 'Lunch',
                'target_nutrients': 'Very High Calorie, Rich in Carbs',
                'calories_range_min': 1000,
                'calories_range_max': 1200,
                'proteins': 50,
                'carbs': 150,
                'fats': 40,
                'body_goal': 'sumo-wrestler'
            },
            {
                'name': 'Hot Pot with Beef, Tofu, and Udon',
                'category': 'Dinner',
                'target_nutrients': 'Very High Calorie, Protein-Rich',
                'calories_range_min': 1200,
                'calories_range_max': 1500,
                'proteins': 60,
                'carbs': 100,
                'fats': 50,
                'body_goal': 'sumo-wrestler'
            },
            {
                'name': 'Fried Tempura and Rice',
                'category': 'Snacks',
                'target_nutrients': 'High Calorie, Rich in Fats',
                'calories_range_min': 500,
                'calories_range_max': 700,
                'proteins': 30,
                'carbs': 60,
                'fats': 20,
                'body_goal': 'sumo-wrestler'
            },
            {
                'name': 'Sweetened Soy Milk',
                'category': 'Drinks',
                'target_nutrients': 'High Calorie, Balanced',
                'calories_range_min': 200,
                'calories_range_max': 300,
                'proteins': 20,
                'carbs': 25,
                'fats': 10,
                'body_goal': 'sumo-wrestler'
            },
        ],
    }

    # Select meal types for the specific body goal
    body_goal_meals = meal_mappings.get(user.body_goal.lower(), [])
    
    for meal_data in body_goal_meals:
        # Create MealType
        meal_type, _ = MealType.objects.get_or_create(
            name=meal_data['name'],
            defaults={
                'category': meal_data['category'],
                'target_nutrients': meal_data['target_nutrients'],
                'calories_range_min': meal_data['calories_range_min'],
                'calories_range_max': meal_data['calories_range_max'],
                'body_goal': meal_data['body_goal']
            }
        )
        
        # Create MealPlan
        MealPlan.objects.create(
            user=user,
            meal_type=meal_type,
            proteins=meal_data['proteins'],
            carbs=meal_data['carbs'],
            fats=meal_data['fats'],
            total_calories=meal_data['calories_range_max'],
            body_goal=user.body_goal.lower()
        )

