from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Advance
from masters.models import Customer
from sales.forms.advance import AdvanceForm, PaymentFormSet, PaymentForm, CustomerForm
from django.forms.models import model_to_dict
from django.http import JsonResponse

import json
from num2words import num2words
import datetime

class AdvanceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_advance", "sales.add_advance", "sales.change_advance", "sales.delete_advance")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Advance details."

class AdvanceDetailView(AdvanceBaseView, DetailView):
    model = Advance
    permission_required = "sales.view_advance"
    template_name = "sales/advance_print.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        amount_words = num2words(self.object.amount, to="cardinal", lang='en_IN').title()
        amount_words = amount_words.replace("AND", "&")
        today = datetime.date.today()
        context["amount_words"] = amount_words
        last_april_date = datetime.date(today.year, 4, 1)
        if last_april_date > today:
            last_april_date = last_april_date.replace(year=today.year - 1)
            context["financial_year"] = f"{last_april_date.year}-{today.strftime('%y')}"
        else:
            context["financial_year"] = f"{today.year}-{today.replace(year=today.year+1).strftime('%y')}"
        return context

class AdvanceListView(AdvanceBaseView, ListView):
    permission_required = "sales.view_advance"
    template_name = "sales/advances.html"
    queryset = Advance.objects.order_by("-date")
    context_object_name = "advances"

class AdvanceCreateView(AdvanceBaseView, CreateView):
    model = Advance
    permission_required = "sales.add_advance"
    template_name = "sales/advance_form.html"
    form_class = AdvanceForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST)
        context["payment_formset"] = PaymentFormSet(self.request.POST)
        if context["customer_form"].is_valid() and context["payment_formset"].is_valid():
            try:
                cust = Customer.objects.get(contact = context["customer_form"].cleaned_data['contact'])
                context["customer_form"] = CustomerForm(self.request.POST, instance=cust)
                customer = context["customer_form"].save()
            except:
                customer = context["customer_form"].save()
            form.instance.customer = customer
            self.object = form.save()
            context["payment_formset"].instance = self.object
            context["payment_formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_formset"] = PaymentFormSet()
        context["payment_form"] = PaymentForm(label_suffix="")
        context["customer_form"] = CustomerForm(label_suffix="")
        try:
            context["id"] = Advance.objects.order_by("pk").last().id + 1
        except:
            context["id"] = 1
        return context
    
    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(AdvanceCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["label_suffix"] = ""
        return form_kwargs

class AdvanceUpdateView(AdvanceBaseView, UpdateView):
    model = Advance
    permission_required = "sales.change_advance"
    template_name = "sales/advance_form.html"
    form_class = AdvanceForm

    def form_valid(self, form):
        context = self.get_context_data()
        context["customer_form"] = CustomerForm(self.request.POST, instance=self.object.customer)
        context["payment_formset"] = PaymentFormSet(self.request.POST, instance=self.object)
        if context["customer_form"].is_valid() and context["payment_formset"].is_valid():
            try:
                cust = Customer.objects.get(contact = context["customer_form"].cleaned_data['contact'])
                context["customer_form"] = CustomerForm(self.request.POST, instance=cust)
                customer = context["customer_form"].save()
            except:
                customer = context["customer_form"].save()
            form.instance.customer = customer
            self.object = form.save()
            context["payment_formset"].save()
            return redirect(self.get_success_url())
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_formset"] = PaymentFormSet(instance=self.object)
        context["payment_form"] = PaymentForm()
        context["customer_form"] = CustomerForm(instance=self.object.customer)
        context["id"] = self.object.id
        return context
    
class AdvanceFetchAjax(AdvanceBaseView, View):
    permission_required = "sales.view_advance"
    def post(self, request, *args, **kwargs):
        id = json.loads(request.body)["id"]
        try:
            advance = Advance.objects.get(pk=id)
            advance_dict = model_to_dict(advance)
        except:
            advance_dict = {}
        return JsonResponse(advance_dict)
