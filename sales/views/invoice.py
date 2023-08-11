from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from masters.models import Customer
from sales.models import Invoice
from sales.forms.invoice import InvoiceForm, CustomerForm, UntaggedForm, ProductFormSet, UntaggedFormSet, AdvanceFormSet, InvoiceAdvanceForm, PaymentFormSet, PaymentForm

class InvoiceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_invoice", "sales.add_invoice", "sales.change_invoice", "sales.delete_invoice")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Invoice details."

class InvoiceListView(InvoiceBaseView, ListView):
    permission_required = "sales.view_invoice"
    template_name = "sales/invoices.html"
    queryset = Invoice.objects.order_by("-date", "-pk")
    context_object_name = "invoices"

class InvoiceCreateView(InvoiceBaseView, CreateView):
    permission_required = "sales.add_invoice"
    template_name = "sales/invoice_form.html"
    form_class = InvoiceForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST)
        context["product_formset"] = ProductFormSet(self.request.POST)
        context["untagged_formset"] = UntaggedFormSet(self.request.POST)
        context["advance_formset"] = AdvanceFormSet(self.request.POST)
        context["payment_formset"] = PaymentFormSet(self.request.POST)
        
        if (context["customer_form"].is_valid() and 
        context["product_formset"].is_valid() and
        context["untagged_formset"].is_valid() and
        context["advance_formset"].is_valid() and
        context["payment_formset"].is_valid()):
            try:
                customer = Customer.objects.get(**context["customer_form"].cleaned_data)
            except:
                customer = context["customer_form"].save()
            
            form.instance.customer = customer
            self.object = form.save()
            context["product_formset"].instance = self.object
            context["product_formset"].save()
            context["untagged_formset"].instance = self.object
            context["untagged_formset"].save()
            context["advance_formset"].instance = self.object
            context["advance_formset"].save()
            context["payment_formset"].instance = self.object
            context["payment_formset"].save()
            return super().form_valid(form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["customer_form"] = CustomerForm(label_suffix="")
        context["untagged_form"] = UntaggedForm(label_suffix="")
        context["product_formset"] = ProductFormSet()
        context["untagged_formset"] = UntaggedFormSet()
        context["advance_formset"] = AdvanceFormSet()
        context["invoice_advance_form"] = InvoiceAdvanceForm()
        context["payment_formset"] = PaymentFormSet()
        context["payment_form"] = PaymentForm(label_suffix="")
        try:
            context["id"] = Invoice.objects.order_by("pk").last().id + 1
        except:
            context["id"] = 1
        return context
    
    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(InvoiceCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["label_suffix"] = ""
        return form_kwargs
