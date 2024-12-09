from django.shortcuts import render # type: ignore
from django.utils import timezone # type: ignore
from django.db import transaction, models # type: ignore
from django.db.models import Case, When, Value, IntegerField # type: ignore
from .models import WorkoutPlan, WorkoutSelectionLog, MealPlan, MealSelectionLog
from .signals import initialize_workouts_for_user, initialize_meals_for_user
from .models import CompletedDay, MoodEntry
import json
import calendar
from datetime import date, timedelta, datetime

from django.http import JsonResponse # type: ignore
from django.views.decorators.http import require_POST # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore


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
    
    # Get month and year from query parameters, default to current if not provided
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    # Convert to integers
    month = int(month) if month else timezone.now().month
    year = int(year) if year else timezone.now().year
    
    # Get calendar context for specified month/year, passing the user
    calendar_context = get_calendar_context(user, year, month)
    
    # Debug prints
    print("Prev Month:", calendar_context['prev_month'])
    print("Next Month:", calendar_context['next_month'])
    print("Current Month:", calendar_context['current_month'])
    
    # Get personalized workouts and meals
    personalized_workouts = get_personalized_workouts(user)
    
    # Create a list of times to match the number of workouts
    workout_times = ["05:30 AM", "06:00 AM", "06:40 AM", "06:10 PM", "06:45 PM"]
    workout_times = workout_times[:len(personalized_workouts)]
    
    # Get calendar context for specified month/year, passing the user
    calendar_context = get_calendar_context(user, year, month)
    
    context = {
        'personalized_workouts': personalized_workouts,
        'workout_times': workout_times,
        'personalized_meals': get_personalized_meals(user),
        # Add calendar context to existing context
        'current_month': calendar_context['current_month'],
        'calendar_days': calendar_context['calendar_days'],
        'prev_month': calendar_context['prev_month'],
        'next_month': calendar_context['next_month']
    }
    return render(request, 'mySchedule.html', context)

def get_personalized_meals(user):
    meal_order = ['Breakfast', 'Lunch', 'Snacks', 'Dinner', 'Drinks']

    user_meals = MealPlan.objects.filter(
        user=user, 
        body_goal=user.body_goal.lower(),
        meal_type__category__in=meal_order
    ).order_by(
        Case(
            *[When(meal_type__category=category, then=Value(i)) for i, category in enumerate(meal_order)],
            output_field=IntegerField()
        )
    )
    
    # If no meals exist, recreate
    if not user_meals.exists():
        initialize_meals_for_user(user)
        user_meals = MealPlan.objects.filter(
            user=user, 
            body_goal=user.body_goal.lower()
        )
    
    # Try to get existing log or create a new one
    try:
        last_selection = MealSelectionLog.objects.get(user=user)
    except MealSelectionLog.DoesNotExist:
        last_selection = None

    # Conditions to regenerate meals
    regenerate_meals = (
        not last_selection or 
        last_selection.date.date() != timezone.now().date() or
        last_selection.user_intensity != user.intensity or 
        last_selection.body_goal != user.body_goal
    )

    with transaction.atomic():
        if regenerate_meals:
            # Select one meal for each category
            personalized_meals = []
            for category in meal_order:
                meal = user_meals.filter(meal_type__category=category).first()
                if meal:
                    personalized_meals.append(meal)

            # Create or update the selection log
            selection_log, created = MealSelectionLog.objects.update_or_create(
                user=user,
                defaults={
                    'date': timezone.now(),
                    'user_intensity': user.intensity,
                    'body_goal': user.body_goal
                }
            )
            
            # Set and save selected meal IDs
            selection_log.set_selected_meals(list(m.id for m in personalized_meals))
            selection_log.save()
        else:
            # Retrieve previously selected meals
            last_selected_meal_ids = last_selection.get_selected_meals()
            personalized_meals = MealPlan.objects.filter(id__in=last_selected_meal_ids)
    
    return personalized_meals

def get_calendar_context(user, year=None, month=None):
     # If no year/month provided, use current
    if year is None:
        year = timezone.now().year
    if month is None:
        month = timezone.now().month
        
    # Previous and next month navigation
    if month > 1:
        prev_month = month - 1
        prev_year = year
    else:
        prev_month = 12
        prev_year = year - 1
    
    if month < 12:
        next_month = month + 1
        next_year = year
    else:
        next_month = 1
        next_year = year + 1
    
    
    # Create calendar object
    cal = calendar.monthcalendar(year, month)
    
    # Prepare calendar days with additional metadata
    calendar_days = []
    today = date.today()
    
    for week in cal:
        for day in week:
            if day != 0:
                current_date = date(year, month, day)
                calendar_days.append({
                    'day': day,
                    'is_today': (current_date.year == today.year and 
                                 current_date.month == today.month and 
                                 current_date.day == today.day),
                    'is_completed': check_day_completed(user, current_date)
                })
    
    # Previous and next month navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    return {
        'current_month': date(year, month, 1),
        'calendar_days': calendar_days,
        'prev_month': {'year': prev_year, 'month': prev_month},
        'next_month': {'year': next_year, 'month': next_month}
    }

def check_day_completed(user, current_date):
    return CompletedDay.objects.filter(user=user, date=current_date).exists()

@csrf_exempt
@require_POST
def mark_day_completed(request):
    user = request.user
    date_str = request.POST.get('date')
    
    try:
        completed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Create or get the CompletedDay object
        CompletedDay.objects.get_or_create(user=user, date=completed_date)
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
def unmark_day_completed(request):
    user = request.user
    date_str = request.POST.get('date')
    
    try:
        completed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Delete the CompletedDay object
        CompletedDay.objects.filter(user=user, date=completed_date).delete()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
@login_required
def save_mood_entry(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            mood_level = data.get('mood_level')
            mood_factors = data.get('mood_factors', [])

            # Create mood entry
            mood_entry = MoodEntry.objects.create(
                user=request.user,
                mood_level=mood_level,
                mood_factors=mood_factors
            )

            return JsonResponse({
                'status': 'success', 
                'message': 'Mood entry saved successfully',
                'id': mood_entry.id
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e)
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def help_page(request):
    return render(request, 'helpPage.html')