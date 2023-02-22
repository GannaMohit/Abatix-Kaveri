from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, AccessMixin
from sales.models import Invoice
from sales.forms.invoice import InvoiceForm, CustomerForm


class InvoiceBaseView(LoginRequiredMixin, PermissionRequiredMixin, AccessMixin):
    permission_required = ("sales.view_invoice", "sales.add_invoice", "sales.change_invoice", "sales.delete_invoice")
    raise_exception = True
    permission_denied_message = "You do not have permission to access Invoice details."


class InvoiceListView(InvoiceBaseView, ListView):
    permission_required = "sales.view_invoice"
    template_name = "sales/invoices.html"
    queryset = Invoice.objects.order_by("-date", "-pk")
    context_object_name = "invoices"


class InvoiceCreateView:
    class Page1(InvoiceBaseView, CreateView):
        permission_required = "sales.add_invoice"
        template_name = "sales/invoice_form_1.html"
        form_class = InvoiceForm

        # success_url = reverse_lazy("invoice_form_2")

        def form_valid(self, form):
            context = self.get_context_data()
            context["customer_form"] = CustomerForm(self.request.POST)
            if context["customer_form"].is_valid():
                try:
                    customer = Customer.objects.get(**context["customer_form"].cleaned_data)
                except:
                    customer = context["customer_form"].save(commit=False)
                form.instance.customer = customer
                self.request.session["customer"] = customer
                self.request.session["invoice_form"] = form
                self.request.session["invoice"] = form.save(commit=False)
                return super().form_valid(form)
            return self.render_to_response(context)

        def get_context_data(self, **kwargs):
            context = super().get_context_data()
            context["customer_form"] = CustomerForm()
            context["id"] = self.request.session.get("invoice", Invoice.objects.order_by("pk").last()).id
            return context

        def get_form(self, form_class=None):
            return self.request.session.get("invoice_form", InvoiceForm())
