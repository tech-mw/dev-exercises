# sns-priority-board

Django（Function-Based View + 一部 Class-Based View）で構築した、簡易社内SNS風Webアプリケーションです。
投稿には「タイトル・本文・画像・通知レベル」を設定でき、ユーザーによる「いいね」や「既読」機能を備えています。
Bootstrap によるシンプルなUIを実装しています。

---

## 主な機能

- ユーザー登録 / ログイン / ログアウト
- 投稿作成（タイトル / 本文 / 画像 / 通知レベル）
- 投稿一覧表示（レベルに応じたスタイル強調）
- 投稿詳細表示
- 削除、更新（自身の投稿分のみ）
- いいね機能・既読機能（簡易的）
- Bootstrap を用いたシンプルな画面設計（UIは最低限）
---

## 想定ユースケース

社内メンバー間での「お知らせ・業務連絡の共有」を目的とした**ミニSNSアプリ**です。
通知レベルの設定で「重要なお知らせ」など優先度が高い情報は表示が強調/目立たせることができるため、**情報の見落としを防ぎつつ、手軽な社内通知ツールとして活用**

---

---

## セットアップ手順
```
# 仮想環境の作成
$ python3 -m venv venv

# 仮想環境の有効化
$ source ./venv/bin/activate

# 必要なパッケージのインストール
$ pip install django pillow
```

---

## 現在の構成
<pre>
.
├── README
├── manage.py
├── media
│ └── images
│     ├── coffee.png
│     └── remote.jpg
├── snsboardapp
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_snsboardmodel_snsimage.py
│   │   ├── 0003_alter_snsboardmodel_snsimage.py
│   │   └── __init__.py
│   ├── models.py
│   ├── static
│   │   └── style.css
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── snsboardproject
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── templates
    ├── base.html
    ├── board.html
    ├── create.html
    ├── delete.html
    ├── detail.html
    ├── login.html
    ├── signup.html
    └── update.html
</pre>

---

## 各画面例
### 新規登録画面
![新規登録画面](./images/signup.png)

### ログイン画面
![ログイン画面](./images/login.png)

### 投稿一覧画面
![投稿一覧](./images/board.png)

### 新規投稿画面
![新規投稿画面](./images/create.png)

### 詳細画面
![詳細画面](./images/detail.png)

### 編集画面
![編集画面](./images/update.png)

### 削除画面
![削除画面](./images/delete.png)

