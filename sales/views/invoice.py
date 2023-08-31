from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from masters.models import Customer
from sales.models import Invoice
from sales.forms.invoice import InvoiceForm, CustomerForm, UntaggedForm, ProductFormSet, UntaggedFormSet, AdvanceFormSet, InvoiceAdvanceForm, PaymentFormSet, PaymentForm

from django.db.models import Q

from num2words import num2words
import datetime

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
    queryset = Invoice.objects.order_by("-invoice_number")
    context_object_name = "invoices"

    def get_queryset(self):
        today = datetime.date.today()
        last_april_date = datetime.date(today.year, 4, 1)
        if last_april_date > today:
            last_april_date = last_april_date.replace(year=today.year - 1)
        
        start_date = self.request.GET.get("start_date", last_april_date.strftime('%Y-%m-%d'))
        end_date = self.request.GET.get("end_date", today.strftime('%Y-%m-%d'))
        search = self.request.GET.get("search", "")
        queryset = Invoice.objects.filter(Q(customer__name__icontains = search) | Q(customer__firm__icontains=search), date__gte=start_date, date__lte=end_date, 
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

class InvoiceCreateView(InvoiceBaseView, CreateView):
    model = Invoice
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
                if context["customer_form"].cleaned_data['contact'] != "":
                    cust = Customer.objects.get(contact = context["customer_form"].cleaned_data['contact'])
                    context["customer_form"] = CustomerForm(self.request.POST, instance=cust)
                    customer = context["customer_form"].save()
                else:
                    customer = context["customer_form"].save()
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
    form_class = InvoiceForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST, instance=self.object.customer)
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
                if context["customer_form"].cleaned_data['contact'] != "":
                    cust = Customer.objects.get(contact = context["customer_form"].cleaned_data['contact'])
                    context["customer_form"] = CustomerForm(self.request.POST, instance=cust)
                    customer = context["customer_form"].save()
                else:
                    customer = context["customer_form"].save()
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
