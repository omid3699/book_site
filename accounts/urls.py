from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

from .views import AddBookView, AllBooksView, RegisterView, UpdateBook, logout

app_name = "accounts"

urlpatterns = [
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("logout/", logout, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("all_books/", AllBooksView.as_view(), name="all_books"),
    path("edit_book/", AddBookView.as_view(), name="add_book"),
    path("edit_book/<int:pk>", UpdateBook.as_view(), name="edit_book"),
]
