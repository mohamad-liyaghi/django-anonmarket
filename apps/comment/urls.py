from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path("add-comment/", views.AddCommentView.as_view(), name="add-comment"),
    path("delete-comment/", views.CommentDeleteView.as_view(), name="delete-comment")
]

