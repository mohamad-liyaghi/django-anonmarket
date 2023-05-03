from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.ChatListView.as_view(), name="chat-list"),

    path("<int:id>/<str:code>/", views.ChatDetailView.as_view(), name="chat-detail"),
    path("<int:participant_id>/<str:participant_token>/create/", views.ChatCreateView.as_view(), name="create-chat"),
]