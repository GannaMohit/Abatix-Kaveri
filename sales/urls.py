from django.urls import path
from .views import InvoiceListView, HomeSaleListView, AdvanceListView, HomeSaleCreateView

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name="invoices"),
    path("home_sales", HomeSaleListView.as_view(), name="home_sales"),
    path("advances", AdvanceListView.as_view(), name="advances"),
    path("home_sale_new", HomeSaleCreateView.as_view(), name="home_sale_new")
]
