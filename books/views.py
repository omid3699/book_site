import os
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView

from .models import Book, Facolty

# Create your views here.


def handle_404_view(request, exception):
    return render(request=request, template_name="404.html", status=404)


@login_required
def home_view(request):
    user = request.user
    books = Book.objects.filter(facolty=user.facolty)
    return render(
        request=request, template_name="books/index.html", context={"books": books}
    )


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(
        request=request, template_name="books/detail.html", context={"book": book}
    )


class FacoltyList(LoginRequiredMixin, ListView):
    template_name = "books/facolty_list.html"
    model = Facolty
    queryset = Facolty.objects.all()
    context_object_name = "facolties"


@login_required
def facolty_book_list(request, pk):
    facolty = get_object_or_404(Facolty, pk=pk)
    books = facolty.books.all()
    return render(
        request=request,
        template_name="books/facolty_book_list.html",
        context={"facolty": facolty, "books": books},
    )


@login_required
def search(request):
    q = request.GET.get("q")
    if q:
        books = Book.objects.filter(
            Q(name__icontains=q) | Q(author_name=q) | Q(description__icontains=q)
        )
    else:
        books = []
    return render(
        request=request,
        template_name="books/search_result.html",
        context={"q": q, "books": books},
    )


@login_required
def update_system(request):
    output = ""
    try:
        if os.name == "nt":
            result = subprocess.run(
                ["start", "setup.bat"], capture_output=True, text=True, check=True
            )
            output += result.stdout
        else:
            result = subprocess.run(
                ["git", "pull"], capture_output=True, text=True, check=True
            )
            output += result.stdout
            result = subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                check=True,
            )
            output += result.stdout
            result = subprocess.run(
                ["python", "-m", "manage.py", "migrate"],
                capture_output=True,
                text=True,
                check=True,
            )
            # Capture the output from stdout
            output += result.stdout
    except subprocess.CalledProcessError as e:
        # Handle the error and capture the output from stderr
        output = f"An error occurred while running git pull: {e.stderr}"

    # Return the output as an HTTP response
    return HttpResponse(f"<pre>{output}</pre>")
