from django.urls import path
from .views import (
    InvoiceListView, InvoiceCreateView,
    HomeSaleListView, HomeSaleCreateView, HomeSaleUpdateView,
    AdvanceListView, AdvanceCreateView, AdvanceUpdateView
)

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name="invoices"),
    path("home_sales", HomeSaleListView.as_view(), name="home_sales"),
    path("advances", AdvanceListView.as_view(), name="advances"),
    path("home_sale/new", HomeSaleCreateView.as_view(), name="home_sale_new"),
    path("home_sale/<int:pk>/edit", HomeSaleUpdateView.as_view(), name="home_sale_edit"),
    path("advance/new", AdvanceCreateView.as_view(), name="advance_new"),
    path("advance/<int:pk>/edit", AdvanceUpdateView.as_view(), name="advance_edit"),
    path("invoice/new/1", InvoiceCreateView.Page1.as_view(), name="invoice_new_1")
]
