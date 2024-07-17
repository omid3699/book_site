from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .models import Book, Facolty

# Create your views here.

# MVC = Model View Controler & MVT = model View Template


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
    context_object_name = "facolty_list"


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
