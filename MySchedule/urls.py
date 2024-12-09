from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from MySchedule import views

app_name = 'MySchedule'

urlpatterns = [
    path('', views.mySched, name='mySched'),
    path('schedule/', views.mySched, name='schedule_view'),  # Use mySched for this route
    path('mark-completed/', views.mark_day_completed, name='mark_day_completed'),
    path('unmark-completed/', views.unmark_day_completed, name='unmark_day_completed'),
    path('save-mood-entry/', views.save_mood_entry, name='save_mood_entry'),
    path('help/', views.help_page, name='help'),
]