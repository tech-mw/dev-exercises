from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect


def signup_func(request):
    """
    新規登録
    """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            User.objects.create_user(username=username, password=password)
            return render(request, 'signup.html', {'success': '新規登録に成功しました。'})
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザーは既に登録されています'})
    return render(request, 'signup.html', {})


def login_func(request):
    """
    ログイン
    """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('board')
        else:
            return render(request, 'login.html', {'context': 'ログインに失敗しました。ユーザー名またはパスワードが正しくありません。'})
    return render(request, 'login.html', {})


def board_func(request):
    """
    投稿の一覧表示
    """
    # 一覧表示
    return render(request, 'board.html', {})
