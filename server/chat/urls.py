from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('init-chat-room/', views.init_chat_room, name='init_chat_room'),
    path('create-chat-room/', views.create_chat_room, name='create_chat_room'),
    path('generate-totp/', views.generate_TOTP, name='generate_TOTP'),
]
