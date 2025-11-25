from django.urls import path
from . import views

app_name = "chat"

# endpoint: api/chat/
urlpatterns = [
    path("chat-rooms/", views.create_chat_room, name="create_chat_room"),
    path('chat-rooms/<int:room_id>/access-code/', views.generate_access_totp, name='generate_access_totp'),
]
