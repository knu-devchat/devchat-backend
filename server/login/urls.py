from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    # Custom simple login/logout pages
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    # API endpoints for frontend-driven OAuth
    path('github/login/', views.github_login, name='github_login'),
    path('github/callback/', views.github_callback, name='github_callback'),
]
