from django.urls import path
from .views import ProductDetailView, ProductFetchAjax, ProductCreateView

urlpatterns = [
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("_fetch_product", ProductFetchAjax.as_view(), name="fetch_product"),
    path("create", ProductCreateView.as_view(), name="product_create")
]
