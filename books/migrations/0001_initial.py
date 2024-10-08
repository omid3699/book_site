# Generated by Django 5.0.4 on 2024-06-02 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Facolty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('author_name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField()),
                ('cover', models.ImageField(upload_to='book_covers')),
                ('pdf', models.FileField(upload_to='pdf_books')),
                ('created', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL)),
                ('facolty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='books.facolty')),
            ],
        ),
    ]
