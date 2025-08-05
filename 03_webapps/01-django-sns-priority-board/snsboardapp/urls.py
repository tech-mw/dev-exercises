from django.urls import path

from .views import (
    BoardCreate,
    BoardDelete,
    BoardUpdate,
    board_func,
    detail_func,
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
    path("board/", board_func, name="board"),
    path("detail/<int:pk>", detail_func, name="detail"),
    path("good/<int:pk>", good_func, name="good"),
    path("read/<int:pk>", read_func, name="read"),
    path("create/", BoardCreate.as_view(), name="create"),
    path("update/<int:pk>", BoardUpdate.as_view(), name="update"),
    path("delete/<int:pk>", BoardDelete.as_view(), name="delete"),
]
