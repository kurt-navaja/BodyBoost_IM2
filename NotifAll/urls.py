from django.contrib import admin
from django.urls import path
# from Notif import settings
from NotifAll import views
from django.conf.urls.static import static

app_name = 'notifAll'

urlpatterns = [
    path('', views.firstP, name='firstP'),
    path('workout/', views.workout, name='workout'),
    path('save_workout/', views.save_workout_preferences, name='save_workout_preferences'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
]
