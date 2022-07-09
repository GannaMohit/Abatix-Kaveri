from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from .models import Product

# Create your views here.
class ProductBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("stock.view_product", "stock.add_product", "stock.change_product", "stock.delete_product")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Stock details."

class ProductDetailView(ProductBaseView, DetailView):
    queryset = Product.objects.filter(sold=False).order_by("pk")
    permission_required = "stock.view_product"
    template_name = "stock/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["first_id"] = self.queryset.first().id
        context["last_id"] = self.queryset.last().id
        return context

    def post(self, request, *args, **kwargs):
        if not self.queryset.exists():
            return redirect("product_new")
        if kwargs["pk"] == 0:
            return redirect("product_detail", pk=request.POST["id"])
        try:
            return self.get(request, *args, **kwargs)
        except:
            if "next" in request.POST:
                temp_qs = self.queryset.filter(id__gt = kwargs["pk"])
                if temp_qs.exists():
                    return redirect("product_detail", pk=temp_qs.first().id)
            else:
                temp_qs = self.queryset.filter(id__lt = kwargs["pk"])
                if temp_qs.exists():
                    return redirect("product_detail", pk=temp_qs.last().id)
        return self.get(request, *args, **kwargs)
