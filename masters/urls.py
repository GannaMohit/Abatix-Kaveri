from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, UnitsFetchAjax, DashboardView, TaxesFetchAjax

urlpatterns = [
    path("", LoginView.as_view(template_name="masters/login.html", redirect_authenticated_user=True), name="login"),
    path("home", HomeView.as_view(), name='home'),
    path("dashboard", DashboardView.as_view(), name='dashboard'),
    path("masters/_fetch_units", UnitsFetchAjax.as_view(), name='fetch_units'),
    path("masters/_fetch_taxes", TaxesFetchAjax.as_view(), name='fetch_taxes')
]
