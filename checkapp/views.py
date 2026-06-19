from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.models import *

from django.conf import settings
from .models import LineUser, LineLog

print("CHECKAPP 起動")


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
# -------------------------
# 登録ページ
# -------------------------

def register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        region = request.POST.get("region")

        LineUser.objects.create(
            user_id=f"web_{name}",
            name=name,
            region=region,
            step="none"
        )

        return render(
            request,
            "checkapp/register_complete.html"
        )

    return render(
        request,
        "checkapp/register.html"
    )
def send_health_check(request):

    users = LineUser.objects.exclude(
    user_id__startswith="web_"
)

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


@handler.add(FollowEvent)
def handle_follow(event):

    user_id = event.source.user_id

    LineUser.objects.get_or_create(
        user_id=user_id
    )

    register_url = " https://nonfrigid-smug-candance.ngrok-free.dev/register"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=
            "友だち追加ありがとうございます。\n\n"
            "下記の登録ページから\n"
            "名前と地域を登録してください。\n\n"
            f"{register_url}"
        )
    )
# -------------------------
# メッセージ受信
# -------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id
    text = event.message.text

    user, created = LineUser.objects.get_or_create(
        user_id=user_id
    )

    print("受信メッセージ:", text)
    
    LineLog.objects.create(
    user=user,
    message_type="text",
    content=text
)

    if text == "元気です":

        reply = TextSendMessage(
            text="それは何よりです。今日も一日頑張りましょう。"
        )

    elif text == "少し疲れています":

        reply = TextSendMessage(
            text="無理をしないでください。休息を取ってください。"
        )

    elif text == "かなり辛いです":

        reply = TextSendMessage(
            text="その原因は体調ですか？ メンタルですか？",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="体調", text="体調")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="メンタル", text="メンタル")
                    ),
                ]
            )
        )

    elif text == "体調":

        reply = TextSendMessage(
            text="病院の受診をおすすめします。無理をせず休養してください。"
        )

    elif text == "メンタル":

        reply = TextSendMessage(
            text="原因は個人ですか？ 仕事ですか？",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="個人", text="個人")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="仕事", text="仕事")
                    ),
                ]
            )
        )

    elif text == "個人":

        reply = TextSendMessage(
            text="身近な方へ相談してください。一人で抱え込まないようにしましょう。"
        )

    elif text == "仕事":

        reply = TextSendMessage(
            text="無理をしないでください。\n委員長が相談に乗ります。\n電話しますか？それともLINEで相談しますか？",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="電話", text="電話")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="LINE", text="LINE")
                    ),
                ]
            )
        )


    elif text == "LINE":
        reply = TextSendMessage(
        text="委員長のLINEへご相談ください。"
    )
    elif text == "電話":
        reply = TextSendMessage(
        text=(
            "委員長へお電話ください。\n\n"
            "【委員長連絡先】\n"
            "090-1234-5678"
        )
    )
    elif text == "無事です":

        reply = TextSendMessage(
            text="無事の確認ができました。GPSを送信してください。"
        )

    elif text == "ケガ":

        reply = TextSendMessage(
            text="周囲へ助けを求めてください。GPSを送信してください。"
        )

    elif text == "危険":

        reply = TextSendMessage(
            text="安全な場所へ避難してください。GPSを送信してください。"
        )

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

    logs = LineLog.objects.all().order_by('-created_at')

    html = "<h1>LINE LOG</h1>"

    for log in logs:

        html += (
            f"<p>"
            f"{log.created_at.strftime('%Y-%m-%d %H:%M')} "
            f"{log.user.name or log.user.user_id} "
            f"{log.content}"
            f"</p>"
        )

    return HttpResponse(html)