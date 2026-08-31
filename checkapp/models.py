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

    # 社員番号（Accountとの連携用）
    login_id = models.CharField(
        max_length=6,
        blank=True,
        null=True
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
    # 電話番号
    phone = models.CharField(
        max_length=20,
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
    # USER または BOT
    sender = models.CharField(
        max_length=10,
        default="USER"
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
    # =====================================
# ログインアカウント
# =====================================

class Account(models.Model):

    AREA_CHOICES = [
        ("北九州", "北九州"),
        ("福岡", "福岡"),
        ("大分", "大分"),
        ("熊本", "熊本"),
        ("長崎", "長崎"),
        ("佐世保", "佐世保"),
    ]

    # 氏名
    name = models.CharField(
        max_length=100
    )

    # 生活地区
    area = models.CharField(
        max_length=20,
        choices=AREA_CHOICES
    )

    # 社員番号（ログインID）
    login_id = models.CharField(
        max_length=6,
        unique=True
    )

    # 生年月日
    birth_date = models.DateField()

    # パスワード
    password = models.CharField(
        max_length=128
    )

    # 利用可能か（退職者は False）
    is_active = models.BooleanField(
        default=True
    )

    # 登録日時
    created_at = models.DateTimeField(
        auto_now_add=True
    )

def __str__(self):
    return f"{self.login_id} {self.name}"

# =====================================
# 過去の配信
# =====================================
class BroadcastHistory(models.Model):

    # 配信タイトル
    title = models.CharField(
        max_length=200
    )

    # 配信内容
    content = models.TextField()

    # 添付PDFのファイル名（PDFなしの場合は空）
    pdf_filename = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    # 配信日時
    sent_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =====================================
# 組合ニュース
# =====================================
class UnionNews(models.Model):

    # 組合ニュースの題名
    title = models.CharField(
        max_length=200
    )

    # 内容（任意）
    content = models.TextField(
        blank=True,
        default=""
    )

    # PDFファイル名
    pdf_filename = models.CharField(
        max_length=255
    )

    # 登録日時
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 更新日時
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
