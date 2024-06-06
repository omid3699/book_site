from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    facolty = models.ForeignKey(
        to="books.Facolty", related_name="users", on_delete=models.CASCADE, null=True
    )
    is_student = models.BooleanField(default=True) # True

    def __str__(self) -> str:
        return self.get_full_name()
