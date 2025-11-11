from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path('login/', views.login_with_github, name='login_with_github'),
    path('logout/', views.logout, name='logout'),
]
