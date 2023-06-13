from django.urls import path
from .views import VoucherListView, VoucherCreateView

urlpatterns = [
    path("", VoucherListView.as_view(), name="vouchers"),
    path("new", VoucherCreateView.as_view(), name="vouchers_new")
]
