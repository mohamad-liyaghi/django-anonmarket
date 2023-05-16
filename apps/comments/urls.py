from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("add/", views.AddCommentView.as_view(), name="add-comment"),
    path("<int:content_type_id>/<object_id>/list/", views.CommentListView.as_view(), name='comment-list'),
    path("<int:comment_id>/update/", views.CommentUpdateView.as_view(), name='update-comment'),
    path("delete-comment/", views.CommentDeleteView.as_view(), name="delete-comment")
]

