from dataclasses import fields

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from books.models import Book, Facolty

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
            "facolty",
        ]


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            "name",
            "author_name",
            "description",
            "cover",
            "pdf",
            "facolty",
        ]

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["facolty"].required = False if self.instance else True


class FacoltyForm(ModelForm):
    class Meta:
        model = Facolty
        fields = ["name"]
