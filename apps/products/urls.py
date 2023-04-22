from django.urls import  path
from .views.product import (
    UserProduct,
    ProductCreateView,
    UpdateProduct,
    DeleteProduct,
    ProductDetail,
    AcceptOrder,
    RejectOrder,
    SendOrder,
    OrderList
)

app_name = "products"

urlpatterns = [
    path("", UserProduct.as_view(), name="list-product"),

    path("add-product/", ProductCreateView.as_view(), name="add-product"),
    path("update-product/<int:id>/<str:slug>/", UpdateProduct.as_view(), name="update-product"),
    path("delete-product/<int:id>/<str:slug>/", DeleteProduct.as_view(), name="delete-product"),

    path("product-detail/<int:id>/<str:slug>/", ProductDetail.as_view(), name="product-detail"),

    path("accept-order/<int:id>/<int:code>/", AcceptOrder.as_view(), name="accept-order"),
    path("reject-order/<int:id>/<int:code>/", RejectOrder.as_view(), name="reject-order"),
    path("send-order/<int:id>/<int:code>/", SendOrder.as_view(), name="send-order"),

    path("orders/", OrderList.as_view(), name="order-list"),


]

