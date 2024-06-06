from django.urls import path

from .views import home_view, book_detail, FacoltyList

app_name = "books"

urlpatterns = [
    path("", home_view, name="home"),
    path("deatil/<int:pk>", book_detail, name="book_detail"),
    path("facolty_list/", FacoltyList.as_view(), name="facolty_list"),
]
