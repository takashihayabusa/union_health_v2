from django.db import models


# =====================================
# LINEユーザー
# =====================================

class LineLog(models.Model):

    # ユーザー
    user = models.ForeignKey(
        LineUser,
        on_delete=models.CASCADE
    )

    # USER または BOT
    sender = models.CharField(
        max_length=10,
        default="USER"
    )

    # 健康・緊急・GPS・電話番号など
    message_type = models.CharField(
        max_length=30
    )

    # メッセージ内容
    content = models.TextField()

    # 日時
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.user} {self.sender}"