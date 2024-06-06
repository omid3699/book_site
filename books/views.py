from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Book, Facolty

# Create your views here.


def home_view(request):
    user = request.user
    books = Book.objects.filter(facolty=user.facolty)
    return render(
        request=request, template_name="books/index.html", context={"books": books}
    )


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(
        request=request, template_name="books/detail.html", context={"book": book}
    )

class FacoltyList(ListView):
    template_name = "books/facolty_list.html"
    model = Facolty
    queryset = Facolty.objects.all()
    context_object_name = "facolty_list"

def facolty_book_list(request, pk):
    facolty = get_object_or_404(Facolty, pk=pk)
    books = facolty.books.all()
    return render(request=request, template_name="books/facolty_book_list.html", context={"facolty":facolty, "books":books})