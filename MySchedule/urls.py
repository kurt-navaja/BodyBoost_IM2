from django.contrib import admin
from django.urls import path
from MySchedule import views

app_name = 'MySchedule'

urlpatterns = [
    path('', views.mySched, name='mySched'),
]