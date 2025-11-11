from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    # Custom simple login/logout pages
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # API endpoints for frontend-driven OAuth
    path('api/auth/github/url/', views.github_auth_url, name='api_github_auth_url'),
    path('api/auth/logout-url/', views.logout_url, name='api_logout_url'),
]
