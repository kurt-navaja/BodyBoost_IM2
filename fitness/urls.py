from django.contrib import admin
from django.urls import path
from fitness import views

app_name = 'fitness'

urlpatterns = [
    path('strengthTraining-beginner/', views.strength, name='strength_beginner'),
    path('strengthTraining-beginner2/', views.strength2, name='strength_beginner2'),
    path('strengthTraining-beginner/progress', views.strength_progress, name='strength_beginner_progress'),
    path('strengthTraining-intermediate/', views.strength_intermediate, name='strength_intermediate'),
    path('strengthTraining-intermediate2/', views.strength_intermediate2, name='strength_intermediate2'),
    path('strengthTraining-intermediate/progress', views.strength_intermediate_progress, name='strength_intermediate_progress'),
    path('strengthTraining-advanced/', views.strength_advanced, name='strength_advanced'),
    path('strengthTraining-advanced2/', views.strength_advanced2, name='strength_advanced2'),
    path('strengthTraining-advanced/progress', views.strength_advanced_progress, name='strength_advanced_progress'),
    path('cardio-beginner/', views.cardio_beginner, name='cardio_beginner'),
    path('cardio-beginner2/', views.cardio_beginner2, name='cardio_beginner2'),
    path('cardio-beginner/progress', views.cardio_beginner_progress, name='cardio_beginner_progress'),
    path('cardio-intermediate/', views.cardio_intermediate, name='cardio_intermediate'),
    path('cardio-intermediate2/', views.cardio_intermediate2, name='cardio_intermediate2'),
    path('cardio-intermediate/progress', views.cardio_intermediate_progress, name='cardio_intermediate_progress'),
    path('cardio-advanced/', views.cardio_advanced, name='cardio_advanced'),
    path('cardio-advanced2/', views.cardio_advanced2, name='cardio_advanced2'),
    path('cardio-advanced/progress', views.cardio_advanced_progress, name='cardio_advanced_progress'),
    path('yoga-beginner/', views.yoga_beginner, name='yoga_beginner'),
    path('yoga-beginner2/', views.yoga_beginner2, name='yoga_beginner2'),
    path('yoga-beginner/progress', views.yoga_beginner_progress, name='yoga_beginner_progress'),
    path('yoga-intermediate/', views.yoga_intermediate, name='yoga_intermediate'),
    path('yoga-intermediate2/', views.yoga_intermediate2, name='yoga_intermediate2'),
    path('yoga-intermediate/progress', views.yoga_intermediate_progress, name='yoga_intermediate_progress'),
    path('yoga-advanced/', views.yoga_advanced, name='yoga_advanced'),
    path('yoga-advanced2/', views.yoga_advanced2, name='yoga_advanced2'),
    path('yoga-advanced/progress', views.yoga_advanced_progress, name='yoga_advanced_progress'),
]