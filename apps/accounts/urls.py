from django.urls import path
from .views import ProfileView, ExchangeView

app_name = "accounts"

urlpatterns = [
    path("profile/<int:id>/<str:token>/", ProfileView.as_view(), name="profile"),
    path("exchange/", ExchangeView.as_view(), name="exchange"),
]