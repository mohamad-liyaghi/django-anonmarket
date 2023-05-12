from django.urls import  path
from .views import forum

app_name = "forums"

urlpatterns = [
    path("", forum.ForumListView.as_view(), name="forum-list"),
    path("create/", forum.ForumCreateView.as_view(), name="create-forum"),

    path("update-forum/<int:id>/<str:slug>/", forum.UpdateForum.as_view(), name="update-forum"),
    path("delete-forum/<int:id>/<str:slug>/", forum.DeleteForum.as_view(), name="delete-forum"),
    
    path("forum-detail/<int:id>/<str:slug>/", forum.ForumDetail.as_view(), name="forum-detail"),
    path("buy-forum/<int:id>/<str:slug>/", forum.BuyForum.as_view(), name="buy-forum"),


]