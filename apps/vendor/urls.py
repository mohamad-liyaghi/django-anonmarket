from django.urls import  path
from . import views

app_name = "vendor"

urlpatterns = [
    path("add-product/", views.AddProduct.as_view(), name="add-product"),
]