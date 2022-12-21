from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("profile/<int:id>/<str:token>/", views.Profile.as_view(), name="profile"),
    path("exchange/", views.Exchange.as_view(), name="exchange"),
]