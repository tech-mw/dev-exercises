from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200)  # タイトル
    body = models.TextField()  # 本文
    summary = models.TextField(blank=True, null=True)  # 要約
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
