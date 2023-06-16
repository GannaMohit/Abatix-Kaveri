from django.urls import path
from .views import VoucherListView, VoucherCreateView, VoucherUpdateView

urlpatterns = [
    path("", VoucherListView.as_view(), name="vouchers"),
    path("new", VoucherCreateView.as_view(), name="vouchers_new"),
    path("<int:pk>/edit", VoucherUpdateView.as_view(), name="voucher_edit")
]
