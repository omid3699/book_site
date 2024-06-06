from django.contrib import admin

from .models import Book, Facolty

# Register your models here.


@admin.register(Facolty)
class FacoltyAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "author_name",
        "cover",
        "pdf",
        "facolty",
    ]
