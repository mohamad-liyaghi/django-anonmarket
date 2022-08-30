from django.urls import  path
from . import views

app_name = "forum"

urlpatterns = [
    path("create-forum/", views.CreateForum.as_view(), name="create-forum"),
]