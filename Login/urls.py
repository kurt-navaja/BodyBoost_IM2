from django.urls import path
from . import views
from .views import login_view, home_view

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgotPassword/', views.forgot_password_view, name='forgotPassword'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
]