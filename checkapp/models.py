from django.db import models


# =====================================
# LINEユーザー
# =====================================

class LineUser(models.Model):

    REGION_CHOICES = [

        ('福岡', '福岡'),
        ('熊本', '熊本'),
        ('長崎', '長崎'),
        ('佐賀', '佐賀'),

    ]

    # LINE userId
    user_id = models.CharField(
        max_length=100,
        unique=True
    )

    # 名前
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # 地域
    region = models.CharField(
        max_length=50,
        choices=REGION_CHOICES,
        blank=True,
        null=True
    )

    # 会話状態
    step = models.CharField(
        max_length=50,
        default='none'
    )

    # 登録日時
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.name:
            return self.name

        return self.user_id


# =====================================
# LINE LOG
# =====================================

class LineLog(models.Model):

    MESSAGE_TYPES = [

        ('text', 'text'),
        ('location', 'location'),

    ]

    # ユーザー
    user = models.ForeignKey(
        LineUser,
        on_delete=models.CASCADE
    )

    # メッセージ種類
    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPES
    )

    # 内容
    content = models.TextField()

    # 日時
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user} - {self.message_type}"