from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from books.models import Book, Facolty

from .forms import BookForm, FacoltyForm, RegisterForm
from .mixins import SuperuserOnlyMixin, SuperuserOrTeacherMixin
from .models import User

# Create your views here.


@login_required
def logout(request):
    auth_logout(request=request)
    return redirect(reverse_lazy("accounts:login"))


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"

    def form_valid(self, form):
        form = form
        return super().form_valid(form)


class AllBooksView(LoginRequiredMixin, SuperuserOrTeacherMixin, ListView):
    template_name = "accounts/all_books.html"
    model = Book
    context_object_name = "books"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Book.objects.all()
        elif not user.is_student:
            return Book.objects.filter(facolty=user.facolty)
        else:
            return redirect(reverse_lazy("books:home"))


class AddBookView(LoginRequiredMixin, SuperuserOrTeacherMixin, CreateView):
    template_name = "accounts/add_book.html"
    form_class = BookForm

    def form_valid(self, form):
        user = self.request.user
        book = form.save(commit=False)
        book.uploaded_by = user
        if not user.is_superuser and not user.student:
            book.facolty = user.facolty
        book.save()
        return redirect(reverse_lazy("accounts:all_books"))


class UpdateBook(LoginRequiredMixin, SuperuserOrTeacherMixin, UpdateView):
    template_name = "accounts/edit_book.html"
    form_class = BookForm
    model = Book

    def form_valid(self, form):
        user = self.request.user
        book = form.save(commit=False)
        book.uploaded_by = user
        if not user.is_superuser and not user.student:
            book.facolty = user.facolty
        book.save()
        return redirect(reverse_lazy("accounts:all_books"))


@login_required
def delete_book(request, pk):
    if not request.user.is_superuser and request.user.is_student:
        return redirect("books:home")
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_superuser:
        if not book.facolty == request.user.facolty:
            return redirect("accounts:all_books")
    book.delete()
    return redirect("accounts:all_books")


class AllFacoltyView(LoginRequiredMixin, SuperuserOnlyMixin, ListView):
    template_name = "accounts/all_facolty.html"
    model = Facolty
    context_object_name = "facolties"


class CreateFacolty(LoginRequiredMixin, SuperuserOnlyMixin, CreateView):
    template_name = "accounts/add_facolty.html"
    form_class = FacoltyForm
    success_url = reverse_lazy("accounts:facolties")


class UpdateFacolty(LoginRequiredMixin, SuperuserOnlyMixin, UpdateView):
    template_name = "accounts/add_facolty.html"
    form_class = FacoltyForm
    model = Facolty
    success_url = reverse_lazy("accounts:facolties")


@login_required
def delete_facolty(request, pk):
    if not request.user.is_superuser:
        return redirect(reverse_lazy("books:home"))
    f = get_object_or_404(Facolty, pk=pk)
    f.delete()
    return redirect(reverse_lazy("accounts:facolties"))


class TeacherList(LoginRequiredMixin, SuperuserOnlyMixin, ListView):
    template_name = "accounts/teacher_list.html"
    model = User
    queryset = User.objects.filter(is_student=False)

    context_object_name = "teachers"


class AddTeacher(LoginRequiredMixin, SuperuserOnlyMixin, CreateView):
    form_class = RegisterForm
    template_name = "accounts/add_teacher.html"
    success_url = reverse_lazy("accounts:teacher_list")

    def form_valid(self, form):

        user = form.save(commit=False)

        user.is_student = False
        user.save()

        return redirect(reverse_lazy("accounts:teacher_list"))


@login_required
def user_actions(request, pk, action):
    if not request.user.is_superuser:
        return redirect(reverse_lazy("books:home"))
    user = get_object_or_404(User, pk=pk)
    match action:
        case "activate":
            user.is_active = True
            user.save()
        case "deactivate":
            user.is_active = False
            user.save()
        case "delete":
            user.delete()
    if not user.is_student:
        return redirect("accounts:teacher_list")
    return redirect("accounts:student_list")


class StudentList(LoginRequiredMixin, SuperuserOnlyMixin, ListView):
    template_name = "accounts/student_list.html"
    model = User
    queryset = User.objects.filter(is_student=True)

    context_object_name = "students"


class AddStudent(LoginRequiredMixin, SuperuserOnlyMixin, CreateView):
    form_class = RegisterForm
    template_name = "accounts/add_student.html"
    success_url = reverse_lazy("accounts:student_list")
