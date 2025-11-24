from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.conf import settings
from django.http import JsonResponse
from urllib.parse import urlencode
import requests
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.conf import settings
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html')

def logout_view(request):
    auth_logout(request)
    return redirect('/')

def current_user(request):
    """현재 로그인된 사용자 정보 반환"""
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_authenticated': True,
        })
    else:
        return JsonResponse({'is_authenticated': False}, status=401)

# github_login, github_callback 함수들 모두 제거
# Github OAuth 로그인 시작
def github_login(request):
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
        "scope": "read:user user:email",
        "state": "github_login_state"
    }
    github_auth_url = "https://github.com/login/oauth/authorize?" + urlencode(params)
    return redirect(github_auth_url)

# GitHub OAuth 콜백 처리
def github_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    
    if not code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)
    
    if state != "github_login_state":
        return JsonResponse({"error": "Invalid state"}, status=400)

    # 1. code로 access_token 요청
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
    )
    
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        return JsonResponse({"error": "Failed to get access token"}, status=400)

    # 2. access_token으로 사용자 정보 요청
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"}
    )
    
    if user_response.status_code != 200:
        return JsonResponse({"error": "Failed to get user info"}, status=400)
    
    user_data = user_response.json()
    
    # 3. 사용자 생성 또는 업데이트
    username = user_data.get("login")
    email = user_data.get("email")
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": user_data.get("name", ""),
        }
    )
    
    # 4. Django 세션으로 로그인 처리
    auth_login(request, user)
    
    # 5. 프론트엔드로 리다이렉트
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    return redirect(f"{frontend_url}/dashboard")