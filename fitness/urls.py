from django.contrib import admin
from django.urls import path
from fitness import views

app_name = 'fitness'

urlpatterns = [
    path('strengthTraining/', views.strength, name='strength')
]