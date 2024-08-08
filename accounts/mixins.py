from django.shortcuts import redirect
from django.urls import reverse_lazy


class SuperuserOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse_lazy("books:home"))
        return super().dispatch(request, *args, **kwargs)


class SuperuserOrTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.is_student:
            return redirect(reverse_lazy("books:home"))
        return super().dispatch(request, *args, **kwargs)


class SuperuserOrOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.is_student:
            return redirect(reverse_lazy("books:home"))

        book = self.get_object()
        if book.uploaded_by != request.user:
            return redirect(reverse_lazy("books:home"))

        return super().dispatch(request, *args, **kwargs)
