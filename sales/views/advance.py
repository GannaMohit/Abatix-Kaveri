from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Advance

class AdvanceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_advance", "sales.add_advance", "sales.change_advance", "sales.delete_advance")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Advance details."

class AdvanceListView(AdvanceBaseView, ListView):
    template_name = "sales/advances.html"
    queryset = Advance.objects.order_by("-date")
    context_object_name = "advances"
