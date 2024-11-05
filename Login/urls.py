from django.urls import path
from . import views
from .views import login_view, home_view

app_name = 'login'

urlpatterns = [
    path('', views.login_view, name='login'),  # Root login
    path('signup/', views.signup_view, name='signup'),  # Signup view
    path('home/', home_view, name='home'),  # Home view
    path('forgotPassword/', views.forgot_password_view, name='forgotPassword'),
    path('forgotPassword2/', views.forgot_password_2_view, name='forgotPassword2'),
    path('forgotPassword3/', views.forgot_password_3_view, name='forgotPassword3'),
]