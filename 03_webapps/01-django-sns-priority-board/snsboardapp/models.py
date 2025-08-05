from django.db import models

CHOICE = (("danger", "高"), ("warning", "中"), ("primary", "低"), ("light", "無"))


class SnsBoardModel(models.Model):
    """
    投稿モデル
    """

    title = models.CharField(max_length=200, verbose_name="タイトル")
    content = models.TextField(verbose_name="内容")
    author = models.CharField(max_length=50, verbose_name="投稿者")
    snsimage = models.ImageField(
        upload_to="images/", verbose_name="画像", null=True, blank=True
    )
    notice_level = models.CharField(
        max_length=50, choices=CHOICE, default="light", verbose_name="通知レベル"
    )
    good = models.IntegerField(
        null=True, blank=True, default=1, verbose_name="いいね数"
    )
    read = models.IntegerField(null=True, blank=True, default=1, verbose_name="既読数")
    read_users = models.TextField(
        null=True, blank=True, default="", verbose_name="既読ユーザー"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    def __str__(self):
        return self.title
