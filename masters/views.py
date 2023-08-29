from django.db.models import Count, Sum
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse, FileResponse, HttpResponse
from .models import Unit, GST_Rate, Customer
from django.core import serializers
from django.templatetags.static import static
from stock.models import Product
from vouchers.models import Voucher

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
    stock = Product.objects.filter(sold=False).values('metal__metal', 'purity__purity', 'type__type', 'category__category').annotate(Count('pk'), Sum('gross_weight'), Sum('studs_weight'), Sum('net_weight'))
    df = pd.DataFrame.from_records(stock)
    df.rename(columns = {'metal__metal':'Metal',
                            'purity__purity': 'Purity',
                            'type__type': 'Type',
                            'category__category':'Category',
                            'pk__count': 'Qty',
                            'gross_weight__sum': 'Gross Wt.',
                            'studs_weight__sum': 'Studding',
                            'net_weight__sum': 'Net Wt.'},
                            inplace=True)
    filename = f"masters/static/masters/excels/stock({today}).xlsx"
    df.to_excel(filename, sheet_name = "stock", header = True, index = False, )
    response = FileResponse(filename=filename, as_attachment=True, content_type='application/ms-excel')
    # response = HttpResponse(open(filename, 'r', encoding=), content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; stock.xlsx'
    return response