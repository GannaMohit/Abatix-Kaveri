from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Customer)
admin.site.register(GST_State)
admin.site.register(GST_Rate)
admin.site.register(HSN)

admin.site.register(Metal)
admin.site.register(Type)
admin.site.register(Purity)
admin.site.register(Category)
admin.site.register(Stud_Type)
admin.site.register(Unit)