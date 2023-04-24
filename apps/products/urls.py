from django.urls import  path
from .views.product import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView,
    AcceptOrder,
    RejectOrder,
    SendOrder,
    OrderList
)
from .views.category import ProductCategoryView

app_name = "products"

urlpatterns = [
    path("list/", ProductListView.as_view(), name="product-list"),

    path("<int:id>/<str:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("create/", ProductCreateView.as_view(), name="create-product"),
    path("<int:id>/<str:slug>/update/", ProductUpdateView.as_view(), name="update-product"),
    path("<int:id>/<str:slug>/delete/", ProductDeleteView.as_view(), name="delete-product"),

    path("<int:id>/<str:slug>/category/", ProductCategoryView.as_view(), name="product-category"),


    path("accept-order/<int:id>/<int:code>/", AcceptOrder.as_view(), name="accept-order"),
    path("reject-order/<int:id>/<int:code>/", RejectOrder.as_view(), name="reject-order"),
    path("send-order/<int:id>/<int:code>/", SendOrder.as_view(), name="send-order"),

    path("orders/", OrderList.as_view(), name="order-list"),


]

