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