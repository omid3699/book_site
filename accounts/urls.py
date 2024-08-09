from django.urls import path, reverse_lazy

from .views import (AddBookView, AddStudent, AddTeacher, AllBooksView,
                    AllFacoltyView, CreateFacolty, LoginView, RegisterView,
                    StudentList, TeacherList, UpdateBook, UpdateFacolty,
                    UserSearchView, delete_book, delete_facolty, logout,
                    user_actions)

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("all_books/", AllBooksView.as_view(), name="all_books"),
    path("edit_book/", AddBookView.as_view(), name="add_book"),
    path("edit_book/<int:pk>", UpdateBook.as_view(), name="edit_book"),
    path("delete_book/<int:pk>", delete_book, name="delete_book"),
    path("facolties/", AllFacoltyView.as_view(), name="facolties"),
    path("facolty/create/", CreateFacolty.as_view(), name="create_facolty"),
    path("facolty/update/<int:pk>", UpdateFacolty.as_view(), name="update_facolty"),
    path("facolty/delete/<int:pk>", delete_facolty, name="delete_facolty"),
    path("teachers/", TeacherList.as_view(), name="teacher_list"),
    path("teachers/add", AddTeacher.as_view(), name="teacher_add"),
    path("students/", StudentList.as_view(), name="student_list"),
    path("students/add", AddStudent.as_view(), name="student_add"),
    path("useractions/<int:pk>/<str:action>", user_actions, name="actions"),
    path("search/", UserSearchView.as_view(), name="search"),
]
