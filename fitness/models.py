from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    BODY_TYPE_CHOICES = [
        ('slim', 'Slim'),
        ('muscular', 'Muscular'),
        ('large', 'Large'),
    ]
    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    GOAL_CHOICES = [
        ('build_muscle', 'Build Muscle'),
        ('lose_weight', 'Lose Weight'),
        ('maintain_fitness', 'Maintain Fitness'),
    ]
    WORKOUT_STYLE_CHOICES = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility/Yoga'),
    ]
    
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVEL_CHOICES)
    fitness_goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    preferred_style = models.CharField(max_length=20, choices=WORKOUT_STYLE_CHOICES)
    health_concerns = models.TextField(blank=True)

class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('flexibility', 'Flexibility'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    thumbnail = models.ImageField(upload_to='exercise_thumbnails/')
