from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Invoice

class InvoiceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_invoice", "stock.add_invoice", "stock.change_invoice", "stock.delete_invoice")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Invoice details."

class InvoiceListView(InvoiceBaseView, ListView):
    template_name = "sales/invoices.html"
    queryset = Invoice.objects.order_by("-date")
    context_object_name = "invoices"
