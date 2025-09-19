# django-llm-summary-notes
Django（CBV） × TextRank での要約生成メモアプリです。
メモには「タイトル・本文・要約」を保存でき、要約は TextRank による自動生成、Bootstrap を用いたカード型UIと フラッシュメッセージで、軽快に操作できます。

---

## 技術スタック
- Backend: Django (CBV)
- Frontend: Bootstrap 5
- Database: SQLite (開発時)
- Auth: Django Auth (個人用認証)
- NLP: sumy (TextRank Summarizer)

---

## 主な機能
### 現在の主な機能
- メモの作成 / 編集 / 削除（CRUD） 
  - 作成時：保存時に要約（抽出型）を自動生成
- 一覧表示（カードレイアウト）
  - ページネーション対応（最大表示数20）
- フラッシュメッセージ
- 検索機能
- 認証機能（個人） 
  - 未ログイン時は認証画面へ誘導
- 単体テスト（unittest）
### 追加予定
- 英語→日本語の翻訳機能
- url貼り付けからの要約生成
- 生成型による要約生成
- など

---

## 想定ユースケース
海外の面白ガジェットなどを見つけた際のメモや翻訳、要約、会議中の議事録メモなど、**情報の取捨選択が必要なメモ管理**を想定しています。個人向け

---

## セットアップ手順
```
# 仮想環境の作成
$ python3 -m venv venv

# 仮想環境の有効化
$ source ./venv/bin/activate

# 必要なパッケージのインストール
$ pip install -r requirements.txt

# .envファイル作成
$ echo "SECRET_KEY='任意の文字列'" > .env

# マイグレーション
$ python manage.py migrate

# 管理ユーザー作成
$ python manage.py createsuperuser

# サンプルデータ投入（任意）
$ python3 manage.py loaddata notes/fixtures/notes_sample.json

# サーバー起動
$ python manage.py runserver

# ブラウザで http://localhost:8000/ にアクセス
```

---

## 現在の構成
<pre>
.
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── notes
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── fixtures
│   │   └── notes_sample.json
│   ├── forms.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── models.py
│   ├── static
│   │   └── notes
│   │       └── css
│   │           ├── common.css
│   │           └── signin.css
│   ├── templates
│   │   ├── 404.html
│   │   └── notes
│   │       ├── base.html
│   │       ├── form.html
│   │       ├── note_confirm_delete.html
│   │       ├── note_detail.html
│   │       ├── note_list.html
│   │       ├── note_signin.html
│   │       └── paging.html
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_note.py
│   ├── urls.py
│   ├── util
│   │  └── summarizer.py
│   └── views.py
├── README.md
└── requirements.txt
</pre>

## スクリーンショット
追加実装後に更新予定