from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("add-article/", views.CreateArticle.as_view(), name="add-article"),
    path("update-article/<int:id>/<str:slug>/", views.UpdateArticle.as_view(), name="update-article"),
    path("delete-article/<int:id>/<str:slug>/", views.DeleteArticle.as_view(), name="delete-article"),
    path("article-detail/<int:id>/<str:slug>/", views.ArticleDetail.as_view(), name="article-detail"),
    path("buy-article/<int:id>/<str:slug>/", views.BuyArticle.as_view(), name="buy-article"),
    path("user-articles/", views.UserArticleList.as_view(), name="user-articles"),
    path("article-publish/<int:id>/<str:slug>/", views.PublishArticle.as_view(), name="article-publish"),

    path("like/<int:id>/<str:slug>/", views.LikeArticle.as_view(), name="like-article"),
    path("dislike/<int:id>/<str:slug>/", views.DisLikeArticle.as_view(), name="dislike-article"),


]