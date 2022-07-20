from django.urls import path
from .views import ProductDetailView, ProductFetchAjax, ProductCreateView, ProductUpdateView

urlpatterns = [
    path("<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("_fetch_product", ProductFetchAjax.as_view(), name="fetch_product"),
    path("new", ProductCreateView.as_view(), name="product_new"),
    path("<int:pk>/edit", ProductUpdateView.as_view(), name="product_edit")
]
