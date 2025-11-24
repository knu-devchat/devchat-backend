from django.urls import path
from . import views

app_name = "login"

# endpoint: auth/
urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('api/user/me/', views.current_user, name='current_user'),
]
