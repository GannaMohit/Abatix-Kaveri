from django.contrib import admin
from .models import *

# Register your models here.
class VoucherProductInline(admin.StackedInline):
    model = Voucher_Product
    extra = 0
    
class VoucherParticularInline(admin.StackedInline):
    model = Particular
    extra = 0

class VoucherAdmin(admin.ModelAdmin):
    inlines = [
        VoucherProductInline,
        VoucherParticularInline
    ]

admin.site.register(Voucher, VoucherAdmin)