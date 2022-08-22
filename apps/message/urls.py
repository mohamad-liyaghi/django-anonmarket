from django.urls import path
from . import views

app_name = "message"

urlpatterns = [
    path("", views.ChatList.as_view(), name="chat-list")
]