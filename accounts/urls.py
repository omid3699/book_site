from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

from .views import logout

app_name = "accounts"

urlpatterns = [
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("logout/", logout, name="logout"),
]
