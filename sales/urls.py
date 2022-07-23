from django.urls import path
from .views import InvoiceListView, HomeSaleListView, AdvanceListView

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name="invoices"),
    path("home_sales", HomeSaleListView.as_view(), name="home_sales"),
    path("advances", AdvanceListView.as_view(), name="advances")
]
