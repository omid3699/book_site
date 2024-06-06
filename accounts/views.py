from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm
from .models import User

# Create your views here.


@login_required
def logout(request):
    auth_logout(request=request)
    return redirect(reverse_lazy("accounts:login"))


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"

    def form_valid(self, form):
        form = form
        return super().form_valid(form)
