# Description: This file is the main URL configuration for the project. It includes the URL configuration for the admin site and the Login app.
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Login.urls", namespace='login')),  # Root URL for login
    path("signup/", include("Signup.urls", namespace='signup')),  # Dedicated URL for signup
    path('notifAll/', include('NotifAll.urls', namespace='notifAll')),
    path('fitness/', include('fitness.urls', namespace='fitness')),
    path('mySchedule/', include('MySchedule.urls', namespace='mySchedule')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)