from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.ChatListView.as_view(), name="chat-list"),

    path("<int:participant_id>/<str:participant_token>/create/", views.ChatCreateView.as_view(), name="create-chat"),
    path("<int:id>/<str:code>/dd", views.ChatDetail.as_view(), name="chat-detail"),

    path("update-message/<int:id>/", views.UpdateMessage.as_view(), name="update-message"),
    path("delete-message/<int:id>/", views.DeleteMessage.as_view(), name="delete-message"),



]