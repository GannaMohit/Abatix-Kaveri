from django.contrib import admin
from .models import *

# Register your models here.
class ProductStudInline(admin.StackedInline):
    model = Stud
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductStudInline
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor)