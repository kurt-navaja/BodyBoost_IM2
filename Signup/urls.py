from django.urls import path
from . import views

app_name = "signup"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  # Root for signup
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('authentication/', views.authentication_view, name='authentication'),
    path('authenticationSuccess/', views.authenticationSuccess_view, name='authenticationSuccess'),
    path('knowMore/', views.knowMore_view, name='knowMore'),
    path('knowMoreSuccess/', views.knowMoreSuccess_view, name='knowMoreSuccess'),
]