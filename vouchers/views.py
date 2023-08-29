from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from vouchers.models import Voucher, Particular, get_voucher_number
from masters.models import Customer
from vouchers.forms import VoucherForm, ParticularForm, ParticularFormSet, CustomerForm, ProductFormSet

from num2words import num2words

class VoucherBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("vouchers.view_voucher", "vouchers.add_voucher", "vouchers.change_voucher", "vouchers.delete_voucher")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Voucher details."

class VoucherDetailView(VoucherBaseView, DetailView):
    model = Voucher
    permission_required = "vouchers.view_voucher"
    template_name = "vouchers/voucher_print.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        amount_words = num2words(self.object.amount, to="cardinal", lang='en_IN').title()
        amount_words = amount_words.replace("AND", "&")
        context["amount_words"] = amount_words
        return context

class VoucherListView(VoucherBaseView, ListView):
    template_name = "vouchers/vouchers.html"
    queryset = Voucher.objects.filter(type='Issue').order_by("-date", "-pk")
    context_object_name = "vouchers"

class VoucherCreateView(VoucherBaseView, CreateView):
    model = Voucher
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
        context["particular_formset"] = ParticularFormSet(self.request.POST)
        context["product_formset"] = ProductFormSet(self.request.POST)
        if context["customer_form"].is_valid() and context["particular_formset"].is_valid() and context["product_formset"].is_valid():
            try:
                cust = Customer.objects.get(contact = context["customer_form"].cleaned_data['contact'])
                context["customer_form"] = CustomerForm(self.request.POST, instance=cust)
                customer = context["customer_form"].save()
            except:
                customer = context["customer_form"].save()
            form.instance.customer = customer
            self.object = form.save()
            context["particular_formset"].instance = self.object
            context["particular_formset"].save()
            context["product_formset"].instance = self.object
            context["product_formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voucher_number_issue"] = get_voucher_number("Issue")
        context["voucher_number_receive"] = get_voucher_number("Receive")
        context["voucher_number_urd"] = get_voucher_number("URD")
        context["customer_form"] = CustomerForm(label_suffix="")
        context["particular_form"] = ParticularForm(label_suffix="")
        context["particular_formset"] = ParticularFormSet()
        context["product_formset"] = ProductFormSet()
        try:
            context["id"] = Voucher.objects.order_by("pk").last().id + 1
        except:
            context["id"] = 1
        return context

class VoucherUpdateView(VoucherBaseView, UpdateView):
    model = Voucher
    permission_required = "vouchers.change_voucher"
    template_name = "vouchers/voucher_form.html"
    form_class = VoucherForm

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(VoucherUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["label_suffix"] = ""
        return form_kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST, instance=self.object.customer)
        context["particular_formset"] = ParticularFormSet(self.request.POST, instance=self.object)
        context["product_formset"] = ProductFormSet(self.request.POST, instance=self.object)
        if context["customer_form"].is_valid() and context["particular_formset"].is_valid() and context["product_formset"].is_valid():
            try:
                cust = Customer.objects.get(contact = context["customer_form"].cleaned_data['contact'])
                context["customer_form"] = CustomerForm(self.request.POST, instance=cust)
                customer = context["customer_form"].save()
            except:
                customer = context["customer_form"].save()
            form.instance.customer = customer
            self.object = form.save()
            context["particular_formset"].save()
            context["product_formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["voucher_number_issue"] = get_voucher_number("Issue")
        context["voucher_number_receive"] = get_voucher_number("Receive")
        context["voucher_number_urd"] = get_voucher_number("URD")
        context["customer_form"] = CustomerForm(label_suffix="", instance=self.object.customer)
        context["particular_form"] = ParticularForm(label_suffix="")
        context["particular_formset"] = ParticularFormSet(instance=self.object)
        context["product_formset"] = ProductFormSet(instance=self.object)
        context["id"] = self.object.id
        return context