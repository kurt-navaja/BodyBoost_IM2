from django.contrib import admin
from django.urls import path
# from Notif import settings
from NotifAll import views
from django.conf.urls.static import static

app_name = 'notifAll'

urlpatterns = [
    path('', views.firstP, name='firstP'),
    path('admin/', admin.site.urls),
    path('workout/', views.workout, name='workout'),
    path('save_workout/', views.save_workout_preferences, name='save_workout_preferences'),
    path('login/', views.login, name='login'),
    path('accountSettings/', views.accountSettings, name='accountSettings'),
    path('progress/', views.progress, name='progress'),
    path('help/', views.help, name='help'),
]
