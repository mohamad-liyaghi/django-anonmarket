from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),

    path("<int:id>/<str:token>/", views.OrderDetail.as_view(), name="order-detail"),

    path("<int:id>/<str:token>/create/", views.OrderCreateView.as_view(), name="create-order"),
    path("<int:id>/<str:token>/delete/", views.OrderDeleteView.as_view(), name="delete-order"),

    path("<int:id>/<str:token>/status/<str:status>/", views.OrderStatusView.as_view(), name="order-status"),

    path("<int:id>/<str:token>/pay/", views.OrderPayView.as_view(), name="pay-order"),
]