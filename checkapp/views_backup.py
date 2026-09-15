from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.models import *

from django.conf import settings
from .models import LineUser


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


# -------------------------
# 表紙
# -------------------------
def home(request):

    return render(request, 'home.html')


# -------------------------
# ユーザー一覧
# -------------------------
def user_list(request):

    users = LineUser.objects.all().order_by('-id')

    return render(
        request,
        'user_list.html',
        {'users': users}
    )

def send_health_check(request):

    users = LineUser.objects.all()

    for user in users:

        user.step = "health_start"
        user.save()

        message = TextSendMessage(

            text=(
                "【健康チェック】\n\n"
                "現在の体調を教えてください。"
            ),

            quick_reply=QuickReply(
                items=[

                    QuickReplyButton(
                        action=MessageAction(
                            label="元気です",
                            text="元気です"
                        )
                    ),

                    QuickReplyButton(
                        action=MessageAction(
                            label="少し疲れています",
                            text="少し疲れています"
                        )
                    ),

                    QuickReplyButton(
                        action=MessageAction(
                            label="かなり辛いです",
                            text="かなり辛いです"
                        )
                    ),

                ]
            )
        )

        line_bot_api.push_message(
            user.user_id,
            message
        )

    return HttpResponse("健康チェック送信完了")

# -------------------------
# 緊急生存確認
# -------------------------
def emergency_send(request):

    users = LineUser.objects.all()

    for user in users:

        message = TextSendMessage(

            text=(
                "緊急生存確認です。\n"
                "現在の状態を選択してください。"
            ),

            quick_reply=QuickReply(
                items=[

                    QuickReplyButton(
                        action=MessageAction(
                            label="無事です",
                            text="無事です"
                        )
                    ),

                    QuickReplyButton(
                        action=MessageAction(
                            label="ケガ",
                            text="ケガ"
                        )
                    ),

                    QuickReplyButton(
                        action=MessageAction(
                            label="危険",
                            text="危険"
                        )
                    ),

                ]
            )
        )

        line_bot_api.push_message(
            user.user_id,
            message
        )

    return HttpResponse("緊急送信完了")


# -------------------------
# callback
# -------------------------
@csrf_exempt
def callback(request):

    body = request.body.decode('utf-8')
    signature = request.META['HTTP_X_LINE_SIGNATURE']

    try:
        handler.handle(body, signature)

    except Exception as e:
        print(e)

    return HttpResponse("OK")


# -------------------------
# メッセージ受信
# -------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id
    text = event.message.text

    # user_id で保存
    user, created = LineUser.objects.get_or_create(
        user_id=user_id
    )

    # -------------------------
    # 元気
    # -------------------------
    if text == "元気です":

        reply = TextSendMessage(
            text=(
                "よかったです。\n"
                "安全を確保してください。\n"
                "よかったらGPSを送ってください。"
            )
        )

    # -------------------------
    # ケガ
    # -------------------------
    elif text == "ケガをしてます":

        reply = TextSendMessage(
            text=(
                "誰か周りにいませんか。\n"
                "助けを求めてください。\n"
                "GPSを送ってください。\n"
                "こちらから関係各所に連絡します。"
            )
        )

    # -------------------------
    # 危険
    # -------------------------
    elif text == "危険です":

        reply = TextSendMessage(
            text=(
                "危険です。\n"
                "すぐに安全なところへ逃げてください。\n"
                "誰か周りにいませんか。\n"
                "皆さんと行動してください。"
            )
        )

    # -------------------------
    # メンタル
    # -------------------------
    elif text == "メンタル":

        reply = TextSendMessage(

            text=(
                "それは個人の問題ですか？\n"
                "それとも会社が原因ですか？"
            ),

            quick_reply=QuickReply(
                items=[

                    QuickReplyButton(
                        action=MessageAction(
                            label="個人",
                            text="個人"
                        )
                    ),

                    QuickReplyButton(
                        action=MessageAction(
                            label="会社",
                            text="会社"
                        )
                    ),

                ]
            )
        )

    # -------------------------
    # 個人
    # -------------------------
    elif text == "個人":

        reply = TextSendMessage(
            text=(
                "身近な方へ相談してください。\n"
                "一人で抱え込まないようにしてください。"
            )
        )

    # -------------------------
    # 会社
    # -------------------------
    elif text == "会社":

        reply = TextSendMessage(
            text=(
                "組合の委員長が相談に乗ります。\n"
                "電話・LINEで相談してください。"
            )
        )

    # -------------------------
    # 緊急
    # -------------------------
    elif text == "無事です":

        reply = TextSendMessage(
            text="無事の確認ができました。"
        )

    elif text == "ケガ":

        reply = TextSendMessage(
            text=(
                "ケガの確認をしました。\n"
                "周囲へ助けを求めてください。"
            )
        )

    elif text == "危険":

        reply = TextSendMessage(
            text=(
                "危険状態です。\n"
                "安全な場所へ避難してください。"
            )
        )

    # -------------------------
    # その他
    # -------------------------
    else:

        reply = TextSendMessage(
            text="メッセージを受信しました。"
        )

    line_bot_api.reply_message(
        event.reply_token,
        reply
    )


# -------------------------
# LINE LOG
# -------------------------
def line_logs(request):

    return HttpResponse("LINE LOG画面")