from django.urls import path
from .views import InvoiceListView, HomeSaleListView, AdvanceListView, HomeSaleCreateView, HomeSaleUpdateView

urlpatterns = [
    path("invoices", InvoiceListView.as_view(), name="invoices"),
    path("home_sales", HomeSaleListView.as_view(), name="home_sales"),
    path("advances", AdvanceListView.as_view(), name="advances"),
    path("home_sale/new", HomeSaleCreateView.as_view(), name="home_sale_new"),
    path("home_sale/<int:pk>", HomeSaleUpdateView.as_view(), name="home_sale_edit")
]
