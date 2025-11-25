# llm/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.chat_message, name='send_message'),
]