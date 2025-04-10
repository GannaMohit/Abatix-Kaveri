from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from .models import Product, Stud
from masters.models import Unit
from django.forms.models import model_to_dict
from django.http import JsonResponse
from .forms import ProductForm, StudFormSet, StudForm, TagDetailsForm, MetalDetailsForm, ProductDetailsForm, MakingDetailsForm
from django.core import serializers

from .tag import PrintTag
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
            return redirect("product_new")
        if kwargs["pk"] == 0: # The goto product implementation
            return redirect("product_detail", pk=request.POST["id"])
        try:
            return self.get(request, *args, **kwargs)
        except:
            if "next" in request.POST: # The next button implementation
                temp_qs = self.queryset.filter(id__gt = kwargs["pk"])
                if temp_qs.exists():
                    return redirect("product_detail", pk=temp_qs.first().id)
            elif "previous" in request.POST: # The previous button implementation
                temp_qs = self.queryset.filter(id__lt = kwargs["pk"])
                if temp_qs.exists():
                    return redirect("product_detail", pk=temp_qs.last().id)
        return self.get(request, *args, **kwargs)

class ProductFetchAjax(ProductBaseView, View):
    permission_required = "stock.view_product"
    def post(self, request, *args, **kwargs):
        id = json.loads(request.body)["id"]
        try:
            product = Product.objects.get(pk=id)
            product_dict = model_to_dict(product)
        except:
            product_dict = {}
        return JsonResponse(product_dict)

class ProductCreateView(ProductBaseView, CreateView):
    model = Product
    permission_required = "stock.add_product"
    template_name = "stock/product_form.html"
    form_class = ProductForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["formset"] = StudFormSet(self.request.POST)
        if context["formset"].is_valid():
            self.object = form.save()
            context["formset"].instance = self.object
            context["formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_details_form"] = TagDetailsForm(label_suffix="")
        context["metal_details_form"] = MetalDetailsForm(label_suffix="")
        context["product_details_form"] = ProductDetailsForm(label_suffix="")
        context["making_details_form"] = MakingDetailsForm(label_suffix="")
        context["formset"] = StudFormSet()
        context["stud_form"] = StudForm(label_suffix="")
        context["units"] = serializers.serialize("json", Unit.objects.all())
        try:
            context["id"] = Product.objects.order_by("pk").last().id + 1
        except:
            context["id"] = 1
        return context

class ProductUpdateView(ProductBaseView, UpdateView):
    model = Product
    permission_required = "stock.change_product"
    template_name = "stock/product_form.html"
    form_class = ProductForm
    queryset = Product.objects.filter(sold=False).order_by("pk")

    def form_valid(self, form):
        context = self.get_context_data()
        context["formset"] = StudFormSet(self.request.POST, instance=self.object)
        if context["formset"].is_valid():
            self.object = form.save()
            context["formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_details_form"] = TagDetailsForm(label_suffix="", instance=self.object)
        context["metal_details_form"] = MetalDetailsForm(label_suffix="", instance=self.object)
        context["product_details_form"] = ProductDetailsForm(label_suffix="", instance=self.object)
        context["making_details_form"] = MakingDetailsForm(label_suffix="", instance=self.object)
        context["formset"] = StudFormSet(instance=self.object)
        context["stud_form"] = StudForm(label_suffix="")
        context["units"] = serializers.serialize("json", Unit.objects.all())
        context["id"] = self.object.id
        return context
