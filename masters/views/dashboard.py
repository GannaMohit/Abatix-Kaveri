from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from stock.models import Product
from django.db.models import Sum


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = "stock.view_product"
    raise_exception = True
    permission_denied_message = "You do not have permission to access Dashboard."


class DashboardListView(DashboardView, ListView):
    queryset = Product.objects.values("metal__metal", "purity__purity", "type__type", "category__category").annotate(Sum("gross_weight"), Sum("net_weight"), Sum("studs_weight")).order_by("-purity__purity")
    context_object_name = "dashboard"
    template_name = "masters/dashboard.html"
