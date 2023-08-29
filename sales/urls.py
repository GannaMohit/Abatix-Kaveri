from django.urls import path
from .views import (
    InvoiceDetailView, InvoiceListView, InvoiceCreateView, InvoiceUpdateView,
    HomeSaleListView, HomeSaleCreateView, HomeSaleUpdateView,
    AdvanceDetailView, AdvanceListView, AdvanceCreateView, AdvanceUpdateView, AdvanceFetchAjax
)

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name="invoices"),
    path("invoices/new", InvoiceCreateView.as_view(), name="invoice_new"),
    path("invoices/<int:pk>/edit", InvoiceUpdateView.as_view(), name="invoice_edit"),
    path("invoices/<int:pk>/print", InvoiceDetailView.as_view(), name="invoice_print"),
    path("advances", AdvanceListView.as_view(), name="advances"),
    path("advances/new", AdvanceCreateView.as_view(), name="advance_new"),
    path("advances/<int:pk>/edit", AdvanceUpdateView.as_view(), name="advance_edit"),
    path("advances/<int:pk>/print", AdvanceDetailView.as_view(), name="advance_print"),
    path("_fetch_advance", AdvanceFetchAjax.as_view(), name="fetch_advance"),   
    path("home_sales", HomeSaleListView.as_view(), name="home_sales"),
    path("home_sales/new", HomeSaleCreateView.as_view(), name="home_sale_new"),
    path("home_sales/<int:pk>/edit", HomeSaleUpdateView.as_view(), name="home_sale_edit"),
]
