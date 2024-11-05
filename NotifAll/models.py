# Homepage/models.py

from django.db import models
from django.conf import settings

class HomepageSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='homepage_settings')
    show_welcome_message = models.BooleanField(default=True)
    theme_preference = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    
    def __str__(self):
        return f"{self.user.email}'s Homepage Settings"
