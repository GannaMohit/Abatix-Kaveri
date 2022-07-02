from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", LoginView.as_view(template_name="authentication/login.html"), name="login")
]
