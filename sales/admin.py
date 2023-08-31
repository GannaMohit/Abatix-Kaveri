from django.contrib import admin
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin


# Register your models here.
class InvoiceProductInline(admin.StackedInline):
    model = Invoice_Product
    extra = 0

class InvoiceUntaggedInline(admin.StackedInline):
    model = Untagged
    extra = 0

class InvoiceAdvanceInline(admin.StackedInline):
    model = Invoice_Advance
    extra = 0

class InvoicePaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    exclude = ('advance',)

class InvoiceAdmin(PermissionRequiredMixin, admin.ModelAdmin):
    permission_required = ''
    inlines = [
        InvoiceProductInline,
        InvoiceUntaggedInline,
        InvoiceAdvanceInline,
        InvoicePaymentInline
    ]

admin.site.register(Invoice, InvoiceAdmin)

class HomeSaleProductInline(admin.StackedInline):
    model = Home_Sale_Product
    extra = 0

class HomeSaleAdmin(admin.ModelAdmin):
    inlines = [
        HomeSaleProductInline
    ]

admin.site.register(Home_Sale, HomeSaleAdmin)

class AdvancePaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    exclude = ('invoice',)

class AdvanceAdmin(admin.ModelAdmin):
    inlines = [
        AdvancePaymentInline
    ]

admin.site.register(Advance, AdvanceAdmin)