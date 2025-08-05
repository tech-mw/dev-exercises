from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import SnsBoardModel


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
    board_list = SnsBoardModel.objects.all().order_by('-created_at')
    return render(request, 'board.html', {'board_list': board_list})


def detail_func(request, pk):
    """
    投稿の詳細表示
    """
    board = SnsBoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'board': board})


def good_func(request, pk):
    """
    いいね機能（簡易）
    """
    board = SnsBoardModel.objects.get(pk=pk)
    board.good += 1
    board.save()
    return redirect('board')


def read_func(request, pk):
    """
    既読機能（簡易）
    """
    board = SnsBoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    # 既に読んでいる場合は何もしない
    if username in board.read_users:
        return redirect('board')
    # 読んでいない場合はカウントを増やす
    board.read += 1
    users = board.read_users.split(',') if board.read_users else []
    if username not in users:
        users.append(username)
        board.read_users = ','.join(users)
        board.save()
    return redirect('board')
