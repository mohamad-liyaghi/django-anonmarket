from django.urls import path
from . import views

app_name = "message"

urlpatterns = [
    path("", views.ChatList.as_view(), name="chat-list"),

    path("get-chat/<int:id>/<str:token>/", views.GetChat.as_view(), name="get-chat"),
    path("chat-detail/<int:id>/<str:code>/", views.ChatDetail.as_view(), name="chat-detail"),

]