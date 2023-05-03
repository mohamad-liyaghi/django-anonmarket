from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chats/<int:id>/<str:code>/', consumers.ChatConsumer.as_asgi()),
]