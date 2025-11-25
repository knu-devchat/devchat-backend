"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_home(request):
    """API 홈페이지"""
    return JsonResponse({
        'message': 'DevChat Backend API',
        'status': 'running',
        'endpoints': {
            'admin': '/admin/',
            'github_login': '/accounts/github/login/',
            'api_chat': '/api/chat/',
            'api_user': '/api/user/',
        }
    })

urlpatterns = [
    path('', api_home, name='api_home'),
    path('admin/', admin.site.urls),
    path('api/chat/', include('chat.urls')),
    path('api/user/', include('login.urls')),
    path('accounts/', include('allauth.urls')),
]
