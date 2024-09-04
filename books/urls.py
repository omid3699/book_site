from django.urls import path

from .views import (
    FacoltyList,
    book_detail,
    facolty_book_list,
    home_view,
    search,
    update_system,
)

app_name = "books"

urlpatterns = [
    path("", home_view, name="home"),
    path("deatil/<int:pk>", book_detail, name="book_detail"),
    path("facolty_list/", FacoltyList.as_view(), name="facolty_list"),
    path("facolty/<int:pk>", facolty_book_list, name="facolty_book_list"),
    path("search/", search, name="search"),
    path("update/", update_system, name="update"),
]
