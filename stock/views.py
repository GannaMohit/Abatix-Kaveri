from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from .models import Product

# Create your views here.
class ProductBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("stock.view_product", "stock.add_product", "stock.change_product", "stock.delete_product")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Stock details."

class ProductDetailView(ProductBaseView, DetailView):
    queryset =  Product.objects.filter(sold=False)
    permission_required = "stock.view_product"
    template_name = "stock/product.html"
