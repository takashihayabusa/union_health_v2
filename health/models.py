from django.db import models


class LineUser(models.Model):

    user_id = models.CharField(max_length=100, unique=True)

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    region = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id