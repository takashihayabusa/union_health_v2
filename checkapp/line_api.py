from django.conf import settings

from linebot import (
    LineBotApi,
    WebhookHandler,
)

line_bot_api = LineBotApi(
    settings.LINE_CHANNEL_ACCESS_TOKEN
)

handler = WebhookHandler(
    settings.LINE_CHANNEL_SECRET
)