from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from urllib.parse import urlencode



# Create your views here.
@ensure_csrf_cookie
def login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'account/login.html')

def logout(request):
    auth_logout(request)
    return redirect(getattr(settings, 'LOGOUT_REDIRECT_URL', '/'))


def home(request):
    return render(request, 'index.html')


def github_auth_url(request):
    next_url = request.GET.get('next', '/')
    # allauth registers the provider login name as 'github_login'
    login_path = reverse('github_login')
    params = {'process': 'login'}
    if next_url:
        params['next'] = next_url
    qs = urlencode(params)
    full = request.build_absolute_uri(login_path) + ('?' + qs if qs else '')
    
    # CSRF 토큰도 함께 반환
    csrf_token = get_token(request)
    return JsonResponse({
        'login_url': full,
        'csrf_token': csrf_token
    })

def logout_url(request):
    try:
        logout_path = reverse('account_logout')
    except Exception:
        # fallback to our local logout path
        logout_path = reverse('login:logout') if False else '/accounts/logout/'
    full = request.build_absolute_uri(logout_path)
    return JsonResponse({'logout_url': full})
