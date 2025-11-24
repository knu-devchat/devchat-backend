"""
ASGI config for server project.

This config uses Django Channels to handle both HTTP and WebSocket.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # chat/routing.py 의 websocket_urlpatterns 사용

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# 기존 Django ASGI 앱 (HTTP용)
django_asgi_app = get_asgi_application()

# Channels 라우터
application = ProtocolTypeRouter(
    {
        # HTTP 요청은 기존 Django가 처리
        "http": django_asgi_app,

        # WebSocket 요청은 chat.routing으로 라우팅
        "websocket": AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)
        ),
    }
)
