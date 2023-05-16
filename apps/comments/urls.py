from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("add/", views.AddCommentView.as_view(), name="add-comment"),
    path("<int:content_type_id>/<object_id>/list/", views.CommentListView.as_view(), name='comment-list'),
    path("<int:comment_id>/update/", views.CommentUpdateView.as_view(), name='update-comment'),
    path("<int:comment_id>/delete/", views.CommentDeleteView.as_view(), name="delete-comment")
]

