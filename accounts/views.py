import os

from django.contrib.auth import aauthenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from pdf2image import convert_from_path
from PIL import Image

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

        # If the user is not a superuser and not a student, assign the user's faculty to the book
        if not user.is_superuser and not user.is_student:
            book.facolty = (
                user.facolty
            )  # Corrected the typo from "facolty" to "faculty"

        # Check if a PDF file was uploaded
        if "pdf" in self.request.FILES:
            pdf_file = self.request.FILES["pdf"]

            # Save the PDF file temporarily
            if isinstance(pdf_file, InMemoryUploadedFile):
                pdf_path = default_storage.save(f"temp/{pdf_file.name}", pdf_file)
                pdf_path = default_storage.path(pdf_path)
            elif isinstance(pdf_file, TemporaryUploadedFile):
                pdf_path = pdf_file.temporary_file_path()
            else:
                pdf_path = None

            if pdf_path:
                # Convert the first page of the PDF to an image
                images = convert_from_path(pdf_path, first_page=0, last_page=1)

                if images:
                    image = images[0]
                    # Save the cover image to the specified path
                    cover_dir = os.path.join("media", "book_covers")
                    os.makedirs(cover_dir, exist_ok=True)
                    cover_path = os.path.join(cover_dir, f"{book.id}_cover.png")
                    image.save(cover_path, "PNG")

                    # Set the cover attribute of the book instance
                    book.cover = f"book_covers/{book.id}_cover.png"

        # Save the book instance
        book.save()

        # Redirect to the 'all_books' view
        return redirect(reverse_lazy("accounts:all_books"))


class UpdateBook(LoginRequiredMixin, SuperuserOrTeacherMixin, UpdateView):
    template_name = "accounts/edit_book.html"
    form_class = BookForm
    model = Book

    def form_valid(self, form):
        user = self.request.user
        book = form.save(commit=False)
        book.uploaded_by = user
        if not user.is_superuser and not user.is_student:
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
    queryset = User.objects.filter(is_student=True, is_superuser=False)

    context_object_name = "students"


class AddStudent(LoginRequiredMixin, SuperuserOnlyMixin, CreateView):
    form_class = RegisterForm
    template_name = "accounts/add_student.html"
    success_url = reverse_lazy("accounts:student_list")


class LoginView(View):
    def get_user(self, username):
        user = None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                ...
        return user

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("books:home"))
        return render(request=request, template_name="accounts/login.html")

    def post(self, request):
        next_page = request.GET.get("next")

        usernme_errors = []
        password_erros = []
        errors = []

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username:
            usernme_errors.append("نام کاربری خالی بوده نمیتواند")
        if not password:
            password_erros.append("لطفا پسورد را وارد کنید")

        user = self.get_user(username=username)
        if not user:
            errors.append("کاربری با مشخصات داده شده پیدا نشد")
        else:
            if user.check_password(password):
                login(request=request, user=user)
                if next_page:
                    return redirect(next_page)

                return redirect(reverse_lazy("books:home"))
            else:
                password_erros.append("پسورد وارد شده اشتباه میباشد")
        return render(
            request=request,
            template_name="accounts/login.html",
            context={
                "username_erros": usernme_errors,
                "password_erros": password_erros,
                "errors": errors,
            },
        )
