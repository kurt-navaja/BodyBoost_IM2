from django.db import models # type: ignore
from django.utils import timezone # type: ignore
from Signup.models import CustomUser
import json

class WorkoutType(models.Model):
    name = models.CharField(max_length=100)
    target_muscles = models.CharField(max_length=200)
    difficulty_level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
    duration = models.IntegerField()  # minutes
    calories_burned = models.IntegerField()
    recommended_weight_range_min = models.FloatField()
    recommended_weight_range_max = models.FloatField()
    body_goal = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.workout_type.name} for {self.user.first_name}"

class WorkoutSelectionLog(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='workout_selection_log')
    date = models.DateTimeField(default=timezone.now)
    user_intensity = models.CharField(max_length=50, blank=True, null=True)
    body_goal = models.CharField(max_length=30, blank=True, null=True)
    selected_workouts = models.TextField(blank=True, null=True)

    def set_selected_workouts(self, workout_ids):
        """Convert list of workout IDs to JSON string"""
        self.selected_workouts = json.dumps(workout_ids)

    def get_selected_workouts(self):
        """Convert JSON string back to list of workout IDs"""
        return json.loads(self.selected_workouts) if self.selected_workouts else []

    def __str__(self):
        return f"Workout Selection for {self.user.first_name} on {self.date}"
    
class MealType(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., Breakfast, Lunch, Dinner, Snack
    target_nutrients = models.CharField(max_length=200)
    calories_range_min = models.IntegerField()
    calories_range_max = models.IntegerField()
    body_goal = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.name} - {self.category}"

class MealPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    proteins = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    total_calories = models.IntegerField()
    body_goal = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.meal_type.name} for {self.user.first_name}"

class MealSelectionLog(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='meal_selection_log')
    date = models.DateTimeField(default=timezone.now)
    user_intensity = models.CharField(max_length=50, blank=True, null=True)
    body_goal = models.CharField(max_length=30, blank=True, null=True)
    selected_meals = models.TextField(blank=True, null=True)

    def set_selected_meals(self, meal_ids):
        self.selected_meals = json.dumps(meal_ids)

    def get_selected_meals(self):
        return json.loads(self.selected_meals) if self.selected_meals else []

    def __str__(self):
        return f"Meal Selection for {self.user.first_name} on {self.date}"
    
class CompletedDay(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    
    class Meta:
        unique_together = ('user', 'date')
        
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
class MoodEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    mood_level = models.CharField(max_length=20)  # Poor, Fair, Good, Great, Excellent
    mood_factors = models.JSONField(default=list)  # Store selected mood factors
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Mood Entries"

    def __str__(self):
        return f"{self.user.username}'s mood on {self.timestamp}: {self.mood_level}"