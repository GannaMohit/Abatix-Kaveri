from django.db.models import Count, Sum
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse, FileResponse
from .models import Unit, GST_Rate, Customer
from django.core import serializers
from stock.models import Product
from vouchers.models import Voucher

from django.conf import settings

import json
import datetime
import pandas as pd

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "masters/home.html"

class UnitsFetchAjax(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        units = serializers.serialize("json", Unit.objects.all())
        units_dict = {"units": json.loads(units)}
        return JsonResponse(units_dict)
    
class TaxesFetchAjax(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        taxes = serializers.serialize("json", GST_Rate.objects.all())
        taxes_dict = {"tax": json.loads(taxes)}
        return JsonResponse(taxes_dict)
    
class CustomerFetchAjax(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        contact = json.loads(request.body)["contact"]
        try:
            customer = Customer.objects.get(contact=contact)
            customer_dict = model_to_dict(customer)
        except:
            customer_dict = {}
        return JsonResponse(customer_dict)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "masters/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.date.today()
        last_april_date = datetime.date(today.year, 4, 1)
        if last_april_date > today:
            last_april_date = last_april_date.replace(year=today.year - 1)
        
        context["start_date"] = self.request.GET.get("start_date", last_april_date.strftime('%Y-%m-%d'))
        context["end_date"] = self.request.GET.get("end_date", today.strftime('%Y-%m-%d'))

        context['metal_opening'] = sum(v.pure_weight for v in Voucher.objects.filter(type="Receive", date__lt=context["start_date"]))
        context['metal_purchase'] = sum(v.pure_weight for v in Voucher.objects.filter(type="Receive", date__gte=context["start_date"], date__lte=context["end_date"]))
        context['metal_sale'] = sum(v.pure_weight for v in Voucher.objects.filter(type="Issue", date__gte=context["start_date"], date__lte=context["end_date"]))
        context['metal_inhand'] = context['metal_opening'] + context['metal_purchase'] - context['metal_sale']

        context["stock"] = Product.objects.filter(sold=False).values('metal__metal', 'purity__purity', 'type__type', 'category__category').annotate(Count('pk'), Sum('gross_weight'), Sum('studs_weight'), Sum('net_weight'))
        return context
    
def dashboard_export(request):
    today = datetime.date.today().strftime("%d-%m-%Y")
    stock = Product.objects.filter(sold=False).values('metal__metal', 'purity__purity', 'type__type', 'category__category').annotate(Count('pk'), Sum('gross_weight'), Sum('studs_weight'), Sum('net_weight'), Sum('pieces'))
    df = pd.DataFrame.from_records(stock)

    df.purity__purity = df.purity__purity.astype(float)
    df.gross_weight__sum = df.gross_weight__sum.astype(float)
    df.studs_weight__sum = df.studs_weight__sum.astype(float)
    df.net_weight__sum = df.net_weight__sum.astype(float)

    df.purity__purity = df.purity__purity.apply(lambda x: round(x, 2))
    df.gross_weight__sum = df.gross_weight__sum.apply(lambda x: round(x, 3))
    df.studs_weight__sum = df.studs_weight__sum.apply(lambda x: round(x, 3))
    df.net_weight__sum = df.net_weight__sum.apply(lambda x: round(x, 3))
    df.rename(columns = {'metal__metal': 'metal',
                            'purity__purity': 'purity',
                            'type__type': 'type',
                            'category__category': 'category',
                            'pk__count': 'qty',
                            'gross_weight__sum': 'gross_weight',
                            'studs_weight__sum': 'studding',
                            'net_weight__sum': 'net_weight',
                            'pieces__sum': 'pieces'},
                            inplace=True)
    filename = settings.MEDIA_ROOT + f"masters/exports/stock({today}).xlsx"
    df.to_excel(filename, header = True, index = False)
    response = FileResponse(open(filename, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f"attachment; filename=stock({today}).xlsx"
    return response

def stock_export(request):
    today = datetime.date.today().strftime("%d-%m-%Y")
    stock = Product.objects.filter(sold=False).values(
        'id', 'register_id', 'metal__metal', 'purity__purity', 'type__type', 'category__category',
        'gross_weight', 'studs_weight', 'less_weight', 'net_weight',
        'rate', 'calculation', 'making_charges', 'wastage', 'mrp',
        'vendor__name', 'purchase_date')
    df = pd.DataFrame.from_records(stock)

    df.purity__purity = df.purity__purity.astype(float)
    df.gross_weight = df.gross_weight.astype(float)
    df.studs_weight = df.studs_weight.astype(float)
    df.net_weight = df.net_weight.astype(float)

    df.purity__purity = df.purity__purity.apply(lambda x: round(x, 2))
    df.gross_weight = df.gross_weight.apply(lambda x: round(x, 3))
    df.studs_weight = df.studs_weight.apply(lambda x: round(x, 3))
    df.net_weight = df.net_weight.apply(lambda x: round(x, 3))
    df.rename(columns = {'metal__metal': 'metal',
                            'purity__purity': 'purity',
                            'type__type': 'type',
                            'category__category': 'category'},
                            inplace=True)
    filename = settings.MEDIA_ROOT + f"masters/exports/fullstock({today}).xlsx"
    df.to_excel(filename, header = True, index = False)
    response = FileResponse(open(filename, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f"attachment; filename=fullstock({today}).xlsx"
    return response