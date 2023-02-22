from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "masters/home.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "masters/dashboard.html"
