from django.urls import path

from .views import (
    BoardCreate,
    DeleteView,
    UpdateView,
    BoardView,
    DetailView,
    good_func,
    login_func,
    logout_func,
    read_func,
    signup_func,
)

urlpatterns = [
    path("signup/", signup_func, name="signup"),
    path("login/", login_func, name="login"),
    path("logout/", logout_func, name="logout"),
    path("board/", BoardView.as_view(), name="board"),
    path("detail/<int:pk>", DetailView.as_view(), name="detail"),
    path("good/<int:pk>", good_func, name="good"),
    path("read/<int:pk>", read_func, name="read"),
    path("create/", BoardCreate.as_view(), name="create"),
    path("update/<int:pk>", UpdateView.as_view(), name="update"),
    path("delete/<int:pk>", DeleteView.as_view(), name="delete"),
]
