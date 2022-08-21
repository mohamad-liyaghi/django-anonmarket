from django.urls import  path
from . import views

app_name = "vendor"

urlpatterns = [
    path("add-product/", views.AddProduct.as_view(), name="add-product"),
    path("update-product/<int:id>/<str:slug>/", views.UpdateProduct.as_view(), name="update-product"),
    path("delete-product/<int:id>/<str:slug>/", views.DeleteProduct.as_view(), name="delete-product"),

    path("product-detail/<int:id>/<str:slug>/", views.ProductDetail.as_view(), name="product-detail"),

    path("like-product/<int:id>/<str:slug>/", views.LikeProduct.as_view(), name="like-product"),
    path("dislike-product/<int:id>/<str:slug>/", views.DisLikeProduct.as_view(), name="dislike-product"),


]