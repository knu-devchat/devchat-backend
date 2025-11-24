from django.urls import path
from . import views

app_name = "login"

# endpoint: auth/
urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/user/me/', views.current_user, name='current_user'),
    
    path('github/login/', views.github_login, name='github_login'),
    path('github/callback/', views.github_callback, name='github_callback'),
    #path('logout/', views.logout, name='logout'),
]
