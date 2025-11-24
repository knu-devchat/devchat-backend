from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.urls import reverse
from urllib.parse import urlencode



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


def github_auth_url(request):
    next_url = request.GET.get('next', '/')
    # allauth registers the provider login name as 'github_login'
    login_path = reverse('github_login')
    params = {'process': 'login'}
    if next_url:
        params['next'] = next_url
        qs = urlencode(params)
        full = request.build_absolute_uri(login_path) + ('?' + qs if qs else '')

        # Return an auto-submitting POST form so the allauth provider flow
        # starts immediately (allauth expects a POST to begin provider auth).
        csrf_token = get_token(request)
        html = f'''<!doctype html>
<html>
    <head><meta charset="utf-8"></head>
    <body>
        <form id="authForm" method="post" action="{full}">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        </form>
        <script>document.getElementById('authForm').submit();</script>
    </body>
</html>'''
        return HttpResponse(html)


def logout_url(request):
    try:
        logout_path = reverse('account_logout')
    except Exception:
        # fallback to our local logout path
        logout_path = reverse('login:logout') if False else '/accounts/logout/'
    full = request.build_absolute_uri(logout_path)
    return JsonResponse({'logout_url': full})
