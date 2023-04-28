from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path("search-result/", views.ProductSearch.as_view(), name="search-product"),
    
    path("<int:id>/<str:token>/", views.OrderDetail.as_view(), name="order-detail"),

    path("<int:id>/<str:token>/create/", views.OrderCreateView.as_view(), name="create-order"),
    path("<int:id>/<str:token>/delete/", views.OrderDeleteView.as_view(), name="delete-order"),

    path("<int:id>/<str:token>/status/<str:status>/", views.OrderStatusView.as_view(), name="order-status"),

    path("<int:id>/<str:token>/pay/", views.OrderPayView.as_view(), name="pay-order"),
    path("filter-category/<int:id>/<str:slug>/", views.FilterCategory.as_view(), name="filter-category"),

    path("cart/", views.Cart.as_view(), name="cart"),

]