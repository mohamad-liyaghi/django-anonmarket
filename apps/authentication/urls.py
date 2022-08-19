from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("profile/<int:id>/<str:token>/", views.Profile.as_view(), name="profile"),
    path("like/<int:id>/<str:token>/", views.Like.as_view(), name="like"),
    path("dislike/<int:id>/<str:token>/", views.DisLike.as_view(), name="dislike"),

]