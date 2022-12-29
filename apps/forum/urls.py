from django.urls import  path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumList.as_view(), name="forum-list"),
    path("user/", views.UserForum.as_view(), name="user-forums"),

    path("search-result/", views.ForumSearch.as_view(), name="search-forum"),
    path("create-forum/", views.CreateForum.as_view(), name="create-forum"),
    path("update-forum/<int:id>/<str:slug>/", views.UpdateForum.as_view(), name="update-forum"),
    path("delete-forum/<int:id>/<str:slug>/", views.DeleteForum.as_view(), name="delete-forum"),
    path("forum-detail/<int:id>/<str:slug>/", views.ForumDetail.as_view(), name="forum-detail"),
    path("buy-forum/<int:id>/<str:slug>/", views.BuyForum.as_view(), name="buy-forum"),


]