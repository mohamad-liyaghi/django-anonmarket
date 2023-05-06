from django.urls import path
from . import views

app_name = "votes"

urlpatterns = [
    path('vote/', views.VoteView.as_view(), name="vote"),
]
