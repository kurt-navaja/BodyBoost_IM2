# Description: This file is the main URL configuration for the project. It includes the URL configuration for the admin site and the Login app.
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Login.urls")),
]