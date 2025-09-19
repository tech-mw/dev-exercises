from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note


class NotesTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user_1", password="pass_1")
        # テストデータ作成
        Note.objects.bulk_create([
            Note(title=f"seed {i}", body=f"body {i}", summary=f"summary {i}")
            for i in range(30)
        ])

    def test_unknown_url_returns_404(self):
        """
        存在しないURLにアクセスした場合、404が返ること
        """
        resp = self.client.get("/__no_such__/")
        self.assertEqual(resp.status_code, 404)

    # ログインしていない場合、ログイン画面にリダイレクトされること
    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("notes:index"))
        # 一覧画面はログイン必須なので、ログイン画面にリダイレクトされること
        # expected_url:最終的にリダイレクトされるURL
        # status_code:最初のレスポンスコード
        # target_status_code:最終的にリダイレクトされるURLのレスポンスコード
        self.assertRedirects(
            resp,
            expected_url=f"{reverse('notes:signin')}?next={reverse('notes:index')}",
            status_code=302,
            target_status_code=200
        )

    def test_list_shows_all_seeds(self):
        """
        一覧画面：登録データ全件取得 + 画面表示件数
        """
        self.client.force_login(self.user)

        # 一覧画面にアクセス
        resp = self.client.get(reverse("notes:index"))
        # status_code 200であること
        self.assertEqual(resp.status_code, 200)
        # 登録データが30件であること
        self.assertEqual(Note.objects.count(), 30)
        # 画面に20件表示されていること（最大表示件数を20にしているため）
        object_list = resp.context["object_list"]
        self.assertEqual(len(object_list), 20)
        # ① 降順② 最大取得件数は20件のため、seed 25が取得されていること
        self.assertEqual(object_list[4].title, "seed 25")
        # ページネーションされていること
        self.assertTrue(resp.context["is_paginated"])
        # 1ページあたりの表示件数が20件であること
        self.assertEqual(resp.context["paginator"].per_page, 20)

    def test_create_invalid_does_not_change_count(self):
        """
        新規作成：失敗（バリデーションエラー）
        """
        self.client.force_login(self.user)
        # 現在のデータ件数を取得
        before = Note.objects.count()
        resp = self.client.post(
            reverse("notes:create"),
            data={"title": "", "body": "x"},  # title 必須想定
        )
        # 200で再表示され、エラーがあること
        self.assertEqual(resp.status_code, 200)
        # formにエラーがあること
        self.assertTrue(resp.context["form"].errors)
        # 作成失敗したためデータ件数が変わっていないこと
        self.assertEqual(Note.objects.count(), before)

    def test_create_success(self):
        """
        新規作成：成功
        """
        self.client.force_login(self.user)
        before = Note.objects.count()
        resp = self.client.post(
            reverse("notes:create"),
            data={"title": "new title", "body": "new body"},
        )
        # 一覧画面にリダイレクトされること
        self.assertRedirects(resp, reverse("notes:index"))
        # 作成成功したためデータ件数が1件増えていること
        self.assertEqual(Note.objects.count(), before + 1)
        # 登録されたデータの内容が正しいこと
        obj = Note.objects.get(title="new title")
        self.assertEqual(obj.body, "new body")

    def test_update_success(self):
        """
        更新：成功
        """
        self.client.force_login(self.user)
        # 更新用データを1件作成
        obj = Note.objects.create(title="t", body="b", summary="s")
        # 更新画面にアクセスして更新
        resp = self.client.post(
            reverse("notes:update", args=[obj.id]),
            data={"title": "updated", "body": "updated body", "summary": obj.summary or ""},
        )
        # 一覧画面にリダイレクトされること
        self.assertRedirects(resp, reverse("notes:index"))
        # データが更新されていること
        obj.refresh_from_db()
        # 更新後の値が設定されていること
        self.assertEqual(obj.title, "updated")
        # 更新後の値が設定されていること
        self.assertEqual(obj.body, "updated body")

    def test_delete_success(self):
        """
        削除：成功
        """
        self.client.force_login(self.user)
        # 削除用データを1件作成
        obj = Note.objects.create(title="del", body="b", summary="s")
        before = Note.objects.count()
        # 削除画面にアクセスして削除
        resp = self.client.post(reverse("notes:delete", args=[obj.id]))
        # 一覧画面にリダイレクトされること
        self.assertRedirects(resp, reverse("notes:index"))
        # データが削除されていること
        self.assertEqual(Note.objects.count(), before - 1)
        # 削除したデータが存在しないこと
        self.assertFalse(Note.objects.filter(id=obj.id).exists())
