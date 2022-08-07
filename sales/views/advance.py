from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Advance
from masters.models import Customer
from sales.forms import AdvanceForm, PaymentFormSet, PaymentForm, CustomerForm

class AdvanceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_advance", "sales.add_advance", "sales.change_advance", "sales.delete_advance")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Advance details."

class AdvanceListView(AdvanceBaseView, ListView):
    template_name = "sales/advances.html"
    queryset = Advance.objects.order_by("-date")
    context_object_name = "advances"

class AdvanceCreateView(AdvanceBaseView, CreateView):
    permission_required = "sales.add_advance"
    template_name = "sales/advance_form.html"
    form_class = AdvanceForm

    def form_valid(self, form):
        context = self.get_context_data()
        advance = form.save(commit=False)
        context["customer_form"] = CustomerForm(self.request.POST)
        if context["customer_form"].is_valid():
            try:
                customer = Customer.objects.get(**context["customer_form"].cleaned_data)
            except:
                customer = context["customer_form"].save(commit=False)
        context["formset"] = PaymentFormSet(self.request.POST, instance=advance)
        if context["formset"].is_valid():
            customer.save()
            advance.customer = customer
            advance.save()
            self.object = advance
            context["formset"].save()
            return super().form_valid(form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = PaymentFormSet()
        context["payment_form"] = PaymentForm()
        context["customer_form"] = CustomerForm()
        context["id"] = Advance.objects.order_by("pk").last().id + 1
        return context
