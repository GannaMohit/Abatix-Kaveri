from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from .models import Product, Stud
from masters.models import Unit
from django.forms.models import model_to_dict
from django.http import JsonResponse
from .forms import ProductForm, StudFormSet, StudForm
from django.core import serializers

import json

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
        if not self.queryset.exists(): # If table empty or all products sold
            return redirect("product_create")
        if kwargs["pk"] == 0: # The goto product implementation
            return redirect("product_detail", pk=request.POST["id"])
        try:
            return self.get(request, *args, **kwargs)
        except:
            if "next" in request.POST: # The next button implementation
                temp_qs = self.queryset.filter(id__gt = kwargs["pk"])
                if temp_qs.exists():
                    return redirect("product_detail", pk=temp_qs.first().id)
            elif "prev" in request.POST: # The previous button implementation
                temp_qs = self.queryset.filter(id__lt = kwargs["pk"])
                if temp_qs.exists():
                    return redirect("product_detail", pk=temp_qs.last().id)
        return self.get(request, *args, **kwargs)

class ProductFetchAjax(ProductBaseView, View):
    permission_required = "stock.view_product"
    def post(self, request, *args, **kwargs):
        id = json.loads(request.body)["id"]
        try:
            product =  Product.objects.get(pk=id)
        except:
            product = {}
        return JsonResponse(model_to_dict(product))

class ProductCreateView(ProductBaseView, TemplateView):
    permission_required = "stock.add_product"
    template_name = "stock/product_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm()
        context["formset"] = StudFormSet()
        context["stud_form"] = StudForm()
        context["units"] = serializers.serialize("json", Unit.objects.all())
        context["last_id"] = Product.objects.order_by("pk").last().id
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["form"] = ProductForm(request.POST)
        if context["form"].is_valid():
            product = context["form"].save(commit=False)
            context["formset"] = StudFormSet(request.POST, instance=product)
            if context["formset"].is_valid():
                product.save()
                context["formset"].save()
                return redirect("product_detail", pk=product.id)
            print(context["formset"].errors)
        print(context["form"].errors)
        return self.render_to_response(context)
