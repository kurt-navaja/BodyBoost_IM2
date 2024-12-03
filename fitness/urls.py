from django.contrib import admin
from django.urls import path
from fitness import views

app_name = 'fitness'

urlpatterns = [
    path('strengthTraining-beginner/', views.strength, name='strength_beginner'),
    path('strengthTraining-beginner2/', views.strength2, name='strength_beginner2'),
    path('strengthTraining-intermediate/', views.strength_intermediate, name='strength_intermediate'),
    path('strengthTraining-intermediate2/', views.strength_intermediate2, name='strength_intermediate2'),
    path('strengthTraining-advanced/', views.strength_advanced, name='strength_advanced'),
    path('strengthTraining-advanced2/', views.strength_advanced2, name='strength_advanced2'),
    path('cardio/', views.cardio, name='cardio')
]