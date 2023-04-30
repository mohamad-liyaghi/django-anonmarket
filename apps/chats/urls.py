from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.ChatListView.as_view(), name="chat-list"),

    path("get-chat/<int:id>/<str:token>/", views.GetChat.as_view(), name="get-chat"),
    path("chat-detail/<int:id>/<str:code>/", views.ChatDetail.as_view(), name="chat-detail"),

    path("update-message/<int:id>/", views.UpdateMessage.as_view(), name="update-message"),
    path("delete-message/<int:id>/", views.DeleteMessage.as_view(), name="delete-message"),



]