from django.urls import path
from . import views
from .views import login_view, home_view

urlpatterns = [
    path('', views.login_view, name='login'),  # Root login
    path('signup/', views.signup_view, name='signup'),  # For /signup/
    path('forgotPassword/', views.forgot_password_view, name='forgotPassword'),
    path('home/', home_view, name='home'),  # Home view
]