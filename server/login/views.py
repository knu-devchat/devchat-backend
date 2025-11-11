from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import HttpResponse, JsonResponse


# Create your views here.
def login(request):
    """
    Renders a simple login page which contains a "Sign in with GitHub" button.
    The template uses `provider_login_url 'github'` (django-allauth) to start OAuth.
    """
    # If user already authenticated, redirect to LOGIN_REDIRECT_URL
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'account/login.html')


def logout(request):
    """Log out the user and redirect to LOGOUT_REDIRECT_URL."""
    auth_logout(request)
    return redirect(getattr(settings, 'LOGOUT_REDIRECT_URL', '/'))


def home(request):
    """Simple home view used as a landing page for LOGIN_REDIRECT_URL."""
    # If you prefer a template, create `templates/index.html` at project root.
    return render(request, 'index.html')


def social_debug(request):
    """Return minimal debug info about GitHub social app configuration.

    Does NOT return the client secret value, only indicates whether it's set.
    Available at /accounts/debug-social/ (only intended for local debugging).
    """
    github = settings.SOCIALACCOUNT_PROVIDERS.get('github', {})
    app = github.get('APP', {}) if isinstance(github, dict) else {}
    client_id = app.get('client_id')
    has_secret = bool(app.get('secret'))
    callback = request.build_absolute_uri('/accounts/github/login/callback/')
    return JsonResponse({'client_id_present': bool(client_id), 'client_id': client_id, 'has_secret': has_secret, 'expected_callback': callback})