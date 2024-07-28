from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from books.views import handle_404_view, home_view

handler404 = handle_404_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", include("books.urls")),
    path("accounts/", include("accounts.urls")),
    path("", home_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
