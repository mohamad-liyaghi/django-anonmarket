from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("add-article/", views.CreateArticle.as_view(), name="add-article")
]