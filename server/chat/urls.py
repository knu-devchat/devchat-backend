from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('create-chat-room/', views.create_chat_room, name='create_chat_room'),
    path('generate-totp/', views.generate_TOTP, name='generate_TOTP'),
]
