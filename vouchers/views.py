from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from vouchers.models import Voucher
from vouchers.forms import VoucherForm

class VoucherBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("vouchers.view_voucher", "vouchers.add_voucher", "vouchers.change_voucher", "vouchers.delete_voucher")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Voucher details."

class VoucherListView(VoucherBaseView, ListView):
    template_name = "vouchers.html"
    queryset = Voucher.objects.filter(type='Issue').order_by("-date", "-pk")
    context_object_name = "vouchers"
