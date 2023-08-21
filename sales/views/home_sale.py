from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Home_Sale
from sales.forms.home_sale import HomeSaleForm, ProductFormSet
from stock.models import Product

class HomeSaleBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_home_sale", "sales.add_home_sale", "sales.change_home_sale", "sales.delete_home_sale")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Home Sale details."

class HomeSaleListView(HomeSaleBaseView, ListView):
    template_name = "sales/home_sales.html"
    queryset = Home_Sale.objects.order_by("-date", "-pk")
    context_object_name = "home_sales"

class HomeSaleCreateView(HomeSaleBaseView, CreateView):
    permission_required = "sales.add_home_sale"
    template_name = "sales/home_sale_form.html"
    form_class = HomeSaleForm
    product_queryset = Product.objects.filter(sold=False)

    def form_valid(self, form):
        context = self.get_context_data()
        home_sale = form.save(commit=False)
        context["formset"] = ProductFormSet(self.request.POST, instance=home_sale, queryset=self.product_queryset)
        if context["formset"].is_valid():
            home_sale.save()
            self.object = home_sale
            context["formset"].save()
            return super().form_valid(form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = ProductFormSet(queryset=self.product_queryset)
        try:
            context["id"] = Home_Sale.objects.order_by("pk").last().id + 1
        except:
            context["id"] = 1
        return context

class HomeSaleUpdateView(HomeSaleBaseView, UpdateView):
    permission_required = "sales.change_home_sale"
    template_name = "sales/home_sale_form.html"
    form_class = HomeSaleForm
    model = Home_Sale
    product_queryset = Product.objects.filter(sold=False)

    def form_valid(self, form):
        context = self.get_context_data()
        home_sale = form.save(commit=False)
        context["formset"] = ProductFormSet(self.request.POST, instance=home_sale)
        if context["formset"].is_valid():
            home_sale.save()
            self.object = home_sale
            context["formset"].save()
            return super().form_valid(form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = ProductFormSet(instance=self.object)
        context["id"] = Home_Sale.objects.order_by("pk").last().id + 1
        return context
