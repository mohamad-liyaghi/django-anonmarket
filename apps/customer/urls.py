from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("search-result/", views.ProductSearch.as_view(), name="search-product"),
    path("add-order/<int:id>/<str:slug>/", views.AddOrder.as_view(), name="add-order"),
    path("delete-order/<int:id>/<str:code>/", views.DeleteOrder.as_view(), name="delete-order"),

    path("order-detail/<int:id>/<str:code>/", views.OrderDetail.as_view(), name="order-detail"),

    path("pay-order/<int:id>/<str:code>/", views.PayOrder.as_view(), name="pay-order"),
    path("filter-category/<int:id>/<str:slug>/", views.FilterCategory.as_view(), name="filter-category"),

    path("cart/", views.Cart.as_view(), name="cart"),

]