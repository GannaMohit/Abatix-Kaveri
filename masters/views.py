from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from .models import Unit
from django.core import serializers

import json

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "masters/home.html"

class UnitsFetchAjax(View):
    def post(self, request, *args, **kwargs):
        units = serializers.serialize("json", Unit.objects.all())
        units_dict = {"units": json.loads(units)}
        return JsonResponse(units_dict)
