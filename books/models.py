from django.db import models

from accounts.models import User

# Create your models here.


class Facolty(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self) -> str:
        return self.name

    def student_count(self):
        return self.users.filter(is_student=True).count()

    def teacher_count(self):
        return self.users.filter(is_student=False).count()


class Book(models.Model):
    name = models.CharField(max_length=150)
    author_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    cover = models.ImageField(upload_to="book_covers", null=True)
    pdf = models.FileField(upload_to="pdf_books")
    facolty = models.ForeignKey(
        to=Facolty, on_delete=models.CASCADE, related_name="books"
    )
    uploaded_by = models.ForeignKey(
        to=User, related_name="books", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
