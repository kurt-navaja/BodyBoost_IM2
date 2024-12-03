from django.db import models
from Signup.models import CustomUser

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