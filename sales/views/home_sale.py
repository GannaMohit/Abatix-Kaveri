from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Home_Sale
from sales.forms.home_sale import HomeSaleForm, ProductFormSet
from stock.models import Product
from django.db.models import Q

import datetime


class HomeSaleBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_home_sale", "sales.add_home_sale", "sales.change_home_sale", "sales.delete_home_sale")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Home Sale details."

class HomeSaleListView(HomeSaleBaseView, ListView):
    template_name = "sales/home_sales.html"
    queryset = Home_Sale.objects.order_by("-pk")
    context_object_name = "home_sales"
    def get_queryset(self):
        today = datetime.date.today()
        last_april_date = datetime.date(today.year, 4, 1)
        if last_april_date > today:
            last_april_date = last_april_date.replace(year=today.year - 1)
        
        start_date = self.request.GET.get("start_date", last_april_date.strftime('%Y-%m-%d'))
        end_date = self.request.GET.get("end_date", today.strftime('%Y-%m-%d'))
        search = self.request.GET.get("search", "")
        queryset = Home_Sale.objects.filter(Q(date__icontains = search) | Q(pk__icontains=search), date__gte=start_date, date__lte=end_date, 
                                          ).order_by("-pk")
        return queryset
    
    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        last_april_date = datetime.date(today.year, 4, 1)
        if last_april_date > today:
            last_april_date = last_april_date.replace(year=today.year - 1)
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get("start_date", last_april_date.strftime('%Y-%m-%d'))
        context["end_date"] = self.request.GET.get("end_date", today.strftime('%Y-%m-%d'))
        context["search"] = self.request.GET.get("search", "")
        return context
    

class HomeSaleCreateView(HomeSaleBaseView, CreateView):
    model = Home_Sale
    permission_required = "sales.add_home_sale"
    template_name = "sales/home_sale_form.html"
    form_class = HomeSaleForm
    product_queryset = Product.objects.filter(sold=False)

    def form_valid(self, form):
        context = self.get_context_data()
        context["formset"] = ProductFormSet(self.request.POST)
        if context["formset"].is_valid():
            self.object = form.save()
            context["formset"].instance = self.object
            context["formset"].save()
            return redirect(self.get_success_url())
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
    model = Home_Sale
    permission_required = "sales.change_home_sale"
    template_name = "sales/home_sale_form.html"
    form_class = HomeSaleForm
    product_queryset = Product.objects.filter(sold=False)

    def form_valid(self, form):
        context = self.get_context_data()
        context["formset"] = ProductFormSet(self.request.POST, instance=self.object)
        if context["formset"].is_valid():
            self.object = form.save()
            context["formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = ProductFormSet(instance=self.object)
        context["id"] = self.object.pk
        return context
