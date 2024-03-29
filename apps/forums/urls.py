from django.urls import  path
from .views import forum
from .views import answers

app_name = "forums"

forum_urlpatterns = [
    path("", forum.ForumListView.as_view(), name="forum-list"),
    path("create/", forum.ForumCreateView.as_view(), name="create-forum"),
    
    path("<int:id>/<str:slug>/", forum.ForumDetailView.as_view(), name="forum-detail"),

    path("<int:id>/<str:slug>/update/", forum.ForumUpdateView.as_view(), name="update-forum"),
    path("<int:id>/<str:slug>/delete/", forum.ForumDeleteView.as_view(), name="delete-forum"),
]

forum_answers_urlpatterns = [
    path("<int:id>/<str:slug>/answers/", answers.ForumAnswerListView.as_view(), name="forum-answer-list"),
    path("<int:id>/<str:slug>/answers/create/", answers.ForumAnswerCreateView.as_view(), name="create-forum-answer"),
    path(
        "<int:id>/<str:slug>/answers/update/<int:answer_id>/<str:answer_token>/", 
        answers.ForumAnswerUpdateView.as_view(), 
        name="update-forum-answer"
    ),
    path(
        "<int:id>/<str:slug>/answers/delete/<int:answer_id>/<str:answer_token>/", 
        answers.ForumAnswerDeleteView.as_view(), 
        name="delete-forum-answer"
    ),
    path(
        "<int:id>/<str:slug>/answers/accept/<int:answer_id>/<str:answer_token>/", 
        answers.ForumAnswerAcceptView.as_view(), 
        name="accept-forum-answer"
    ),
]

urlpatterns = [
    *forum_urlpatterns,
    *forum_answers_urlpatterns
]