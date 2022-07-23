from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Home_Sale

class HomeSaleBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_home_sale", "sales.add_home_sale", "sales.change_home_sale", "sales.delete_home_sale")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Home Sale details."

class HomeSaleListView(HomeSaleBaseView, ListView):
    template_name = "sales/home_sales.html"
    queryset = Home_Sale.objects.order_by("-date")
    context_object_name = "home_sales"
