from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="article-list"),

    path("create/", views.ArticleCreateView.as_view(), name="create-article"),
    
    path("<int:id>/<str:slug>/update/", views.UpdateArticle.as_view(), name="update-article"),
    path("<int:id>/<str:slug>/delete/", views.DeleteArticle.as_view(), name="delete-article"),

    path("<int:id>/<str:slug>/", views.ArticleDetailView.as_view(), name="article-detail"),
    path("<int:id>/<str:slug>/purchase/", views.ArticlePurchaseView.as_view(), name="purchase-article"),


]