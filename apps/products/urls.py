from django.urls import  path
from .views.product import (
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView,
    SendOrder,
    OrderList
)
from django.views.generic import RedirectView
from .views.category import ProductCategoryView

app_name = "products"

urlpatterns = [
    path("", RedirectView.as_view(url='/'), name="product-list"),

    path("<int:id>/<str:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("create/", ProductCreateView.as_view(), name="create-product"),
    path("<int:id>/<str:slug>/update/", ProductUpdateView.as_view(), name="update-product"),
    path("<int:id>/<str:slug>/delete/", ProductDeleteView.as_view(), name="delete-product"),

    path("<int:id>/<str:slug>/category/", ProductCategoryView.as_view(), name="product-category"),

    path("send-order/<int:id>/<int:code>/", SendOrder.as_view(), name="send-order"),

    path("orders/", OrderList.as_view(), name="order-list"),


]

