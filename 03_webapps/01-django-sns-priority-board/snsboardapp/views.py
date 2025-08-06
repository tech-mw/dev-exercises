from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .models import SnsBoardModel


def signup_func(request):
    """
    ユーザー新規登録
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            User.objects.create_user(username=username, password=password)
            return render(
                request, "signup.html", {"success": "新規登録に成功しました。"}
            )
        except IntegrityError:
            return render(
                request, "signup.html", {"error": "このユーザーは既に登録されています"}
            )
    return render(request, "signup.html", {})


def login_func(request):
    """
    ログイン
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("board")
        else:
            return render(
                request,
                "login.html",
                {
                    "context": "ログインに失敗しました。ユーザー名またはパスワードが正しくありません。"
                },
            )
    return render(request, "login.html", {})


def logout_func(request):
    """
    ログアウト
    """
    logout(request)
    return redirect("login")


class BoardView(generic.ListView):
    model = SnsBoardModel
    template_name = "board.html"
    context_object_name = "board_list"
    ordering = ["-created_at"]
    paginate_by = 5


class DetailView(generic.DetailView):
    model = SnsBoardModel
    template_name = "detail.html"
    context_object_name = "board"


def good_func(request, pk):
    """
    いいね機能（簡易）
    """
    board = SnsBoardModel.objects.get(pk=pk)
    board.good += 1
    board.save()
    return redirect("board")


def read_func(request, pk):
    """
    既読機能（簡易）
    """
    board = SnsBoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in board.read_users:
        return redirect("board")
    board.read += 1
    users = board.read_users.split(",") if board.read_users else []
    if username not in users:
        users.append(username)
        board.read_users = ",".join(users)
        board.save()
    return redirect("board")


class BoardCreate(generic.CreateView):
    """
    新規投稿作成画面
    """
    template_name = "create.html"
    model = SnsBoardModel
    fields = ("title", "content", "author", "snsimage", "notice_level")
    success_url = reverse_lazy("board")


class UpdateView(generic.UpdateView):
    """
    投稿更新
    """
    template_name = "update.html"
    model = SnsBoardModel
    fields = ("title", "content", "snsimage", "notice_level")
    success_url = reverse_lazy("board")


class DeleteView(generic.DeleteView):
    """
    投稿削除
    """
    template_name = "delete.html"
    model = SnsBoardModel
    success_url = reverse_lazy("board")
