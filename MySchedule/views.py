from django.shortcuts import render, redirect
from django.http import HttpResponse

def mySched(request):
    return render(request, 'mySchedule.html')