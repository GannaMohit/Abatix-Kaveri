from django.urls import path
from .views import ProductDetailView, ProductFetchAjax

urlpatterns = [
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("_fetch_product", ProductFetchAjax.as_view(), name="fetch_product")
]
