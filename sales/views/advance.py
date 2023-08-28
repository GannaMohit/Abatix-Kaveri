from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Advance
from masters.models import Customer
from sales.forms.advance import AdvanceForm, PaymentFormSet, PaymentForm, CustomerForm
from django.forms.models import model_to_dict
from django.http import JsonResponse

import json

class AdvanceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_advance", "sales.add_advance", "sales.change_advance", "sales.delete_advance")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Advance details."

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
                customer = Customer.objects.get(**context["customer_form"].cleaned_data)
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
        context["customer_form"] = CustomerForm(self.request.POST, instance=self.object)
        context["payment_formset"] = PaymentFormSet(self.request.POST, instance=self.object)
        if context["customer_form"].is_valid() and context["payment_formset"].is_valid():
            try:
                customer = Customer.objects.get(**context["customer_form"].cleaned_data)
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
