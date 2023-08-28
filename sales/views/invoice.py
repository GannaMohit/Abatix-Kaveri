from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from masters.models import Customer
from sales.models import Invoice
from sales.forms.invoice import InvoiceForm, CustomerForm, UntaggedForm, ProductFormSet, UntaggedFormSet, AdvanceFormSet, InvoiceAdvanceForm, PaymentFormSet, PaymentForm

from num2words import num2words

class InvoiceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_invoice", "sales.add_invoice", "sales.change_invoice", "sales.delete_invoice")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Invoice details."

class InvoiceDetailView(InvoiceBaseView, DetailView):
    model = Invoice
    permission_required = "sales.view_invoice"
    template_name = "sales/invoice_print.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        amount_words = num2words(self.object.amount, to="cardinal", lang='en_IN').title()
        amount_words = amount_words.replace("AND", "&")
        context["amount_words"] = amount_words
        return context

class InvoiceListView(InvoiceBaseView, ListView):
    permission_required = "sales.view_invoice"
    template_name = "sales/invoices.html"
    queryset = Invoice.objects.order_by("-date", "-pk")
    context_object_name = "invoices"

class InvoiceCreateView(InvoiceBaseView, CreateView):
    model = Invoice
    permission_required = "sales.add_invoice"
    template_name = "sales/invoice_form.html"
    success_url = 'invoices'
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
            return redirect(self.get_success_url())
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
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["label_suffix"] = ""
        return form_kwargs
    
class InvoiceUpdateView(InvoiceBaseView, UpdateView):
    model = Invoice
    permission_required = "sales.change_invoice"
    template_name = "sales/invoice_form.html"
    success_url = 'invoices'
    form_class = InvoiceForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST, instance=self.object)
        context["product_formset"] = ProductFormSet(self.request.POST, instance=self.object)
        context["untagged_formset"] = UntaggedFormSet(self.request.POST, instance=self.object)
        context["advance_formset"] = AdvanceFormSet(self.request.POST, instance=self.object)
        context["payment_formset"] = PaymentFormSet(self.request.POST, instance=self.object)
        
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
            context["product_formset"].save()
            context["untagged_formset"].save()
            context["advance_formset"].save()
            context["payment_formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["customer_form"] = CustomerForm(label_suffix="", instance=self.object.customer)
        context["untagged_form"] = UntaggedForm(label_suffix="")
        context["product_formset"] = ProductFormSet(instance=self.object)
        context["untagged_formset"] = UntaggedFormSet(instance=self.object)
        context["advance_formset"] = AdvanceFormSet(instance=self.object)
        context["invoice_advance_form"] = InvoiceAdvanceForm()
        context["payment_formset"] = PaymentFormSet(instance=self.object)
        context["payment_form"] = PaymentForm(label_suffix="")
        context["id"] = self.object.id

        return context
    
    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["label_suffix"] = ""
        return form_kwargs
