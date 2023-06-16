from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from vouchers.models import Voucher, Particular
from masters.models import Customer
from vouchers.forms import VoucherForm, ParticularForm, ParticularFormSet, CustomerForm

class VoucherBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("vouchers.view_voucher", "vouchers.add_voucher", "vouchers.change_voucher", "vouchers.delete_voucher")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Voucher details."

class VoucherListView(VoucherBaseView, ListView):
    template_name = "vouchers/vouchers.html"
    queryset = Voucher.objects.filter(type='Issue').order_by("-date", "-pk")
    context_object_name = "vouchers"

class VoucherCreateView(VoucherBaseView, CreateView):
    permission_required = "vouchers.add_voucher"
    template_name = "vouchers/voucher_form.html"
    form_class = VoucherForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(VoucherCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["label_suffix"] = ""
        return form_kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST)
        if context["customer_form"].is_valid():
            context["formset"] = ParticularFormSet(self.request.POST)
            if context["formset"].is_valid():
                try:
                    customer = Customer.objects.get(**context["customer_form"].cleaned_data)
                except:
                    customer = context["customer_form"].save()
                form.instance.customer = customer
                self.object = form.save()
                context["formset"].instance = self.object
                context["formset"].save()
                return super().form_valid(form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer_form"] = CustomerForm(label_suffix="")
        context["particular_form"] = ParticularForm(label_suffix="")
        context["formset"] = ParticularFormSet()
        try:
            context["id"] = Voucher.objects.order_by("pk").last().id + 1
        except:
            context["id"] = 1
        return context
