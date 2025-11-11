from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import HttpResponse, JsonResponse


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'account/login.html')

def logout(request):
    auth_logout(request)
    return redirect(getattr(settings, 'LOGOUT_REDIRECT_URL', '/'))


def home(request):
    return render(request, 'index.html')
