from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, DashboardListView

urlpatterns = [
    path("", LoginView.as_view(template_name="masters/login.html", redirect_authenticated_user=True), name="login"),
    path("home", HomeView.as_view(), name='home'),
    path("dashboard", DashboardListView.as_view(), name='dashboard'),
]
