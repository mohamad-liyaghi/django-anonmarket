from django.urls import  path
from . import views

app_name = "vendor"

urlpatterns = [
    path("", views.UserProduct.as_view(), name="list-product"),

    path("add-product/", views.AddProduct.as_view(), name="add-product"),
    path("update-product/<int:id>/<str:slug>/", views.UpdateProduct.as_view(), name="update-product"),
    path("delete-product/<int:id>/<str:slug>/", views.DeleteProduct.as_view(), name="delete-product"),

    path("product-detail/<int:id>/<str:slug>/", views.ProductDetail.as_view(), name="product-detail"),

    path("like-product/<int:id>/<str:slug>/", views.LikeProduct.as_view(), name="like-product"),
    path("dislike-product/<int:id>/<str:slug>/", views.DisLikeProduct.as_view(), name="dislike-product"),

    path("accept-order/<int:id>/<int:code>/", views.AcceptOrder.as_view(), name="accept-order"),
    path("reject-order/<int:id>/<int:code>/", views.RejectOrder.as_view(), name="reject-order"),
    path("send-order/<int:id>/<int:code>/", views.SendOrder.as_view(), name="send-order"),


    path("orders/", views.OrderList.as_view(), name="order-list"),


]