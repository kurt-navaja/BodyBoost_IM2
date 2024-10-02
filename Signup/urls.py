from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('authentication/', views.authentication_view, name='authentication'),
    path('authenticationSuccess/', views.authenticationSuccess_view, name='authenticationSuccess'),
    path('knowMore/', views.knowMore_view, name='knowMore'),
]