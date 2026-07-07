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

    return render(
        request,
        "checkapp/home.html"
    )

# -------------------------
# ユーザー一覧
# -------------------------
def user_list(request):

    users = (
        LineUser.objects
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "checkapp/user_list.html",
        {
            "users": users,
        }
    )
# -------------------------
# 登録
# -------------------------
def register(request):

    # GETでもPOSTでも user_id を取得
    user_id = request.GET.get("user_id") or request.POST.get("user_id")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        region = request.POST.get("region", "").strip()

        if not name or not region:
            return render(
                request,
                "checkapp/register.html",
                {
                    "error": "名前と地域を入力してください。",
                    "user_id": user_id,
                }
            )

        LineUser.objects.update_or_create(
            user_id=user_id,
            defaults={
                "name": name,
                "region": region,
            }
        )

        return render(
            request,
            "checkapp/register_complete.html"
        )

    return render(
        request,
        "checkapp/register.html",
        {
            "user_id": user_id,
        }
    )

# -------------------------
# 健康チェック送信
# -------------------------
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

        try:
            line_bot_api.push_message(
                user.user_id,
                message
            )
            print("送信成功:", user.user_id)

        except Exception as e:
            print("送信失敗:", user.user_id)
            print(e)

    return HttpResponse("健康チェック送信完了")


# -------------------------
# 緊急生存確認
# -------------------------
def emergency_send(request):

    users = LineUser.objects.exclude(
        user_id__startswith="web_"
    )

    for user in users:

        print("送信先:", user.name, user.user_id)

        message = TextSendMessage(
            text=(
                "【緊急生存確認】\n\n"
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

        try:
            line_bot_api.push_message(
                user.user_id,
                message
            )

            print("送信成功:", user.user_id)

        except Exception as e:

            print("送信失敗:", user.user_id)
            print(e)

    return HttpResponse("緊急生存確認を送信しました")

# -------------------------
# Callback
# -------------------------
@csrf_exempt
def callback(request):

    body = request.body.decode("utf-8")
    signature = request.META.get("HTTP_X_LINE_SIGNATURE", "")

    try:
        handler.handle(body, signature)

    except Exception as e:
        print("Callback Error:", e)

    return HttpResponse("OK")
@handler.add(FollowEvent)
def handle_follow(event):

    user_id = event.source.user_id

    LineUser.objects.get_or_create(
        user_id=user_id
    )

    register_url = (
    f"https://nonfrigid-smug-candance.ngrok-free.dev/register?user_id={user_id}"
    )

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


    if text == "元気です":

        reply = TextSendMessage(
            text="それは何よりです。今日も一日頑張りましょう。"
        )

        LineLog.objects.create(
            user=user,
            sender="BOT",
            message_type="text",
            content="それは何よりです。今日も一日頑張りましょう。"
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
        
        line_bot_api.reply_message(
        event.reply_token,
        reply
        )

    elif text == "体調":

        reply = TextSendMessage(
            text="無理をせず、病院の受診も検討してください。お大事になさってください。"
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "メンタル":

        reply = TextSendMessage(
            text="原因を教えてください。",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(
                            label="個人的な悩み",
                            text="個人的な悩み"
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label="仕事の悩み",
                            text="仕事の悩み"
                        )
                    ),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "個人的な悩み":

        reply = TextSendMessage(
            text="一人で抱え込まず、信頼できる方へ相談してください。"
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "仕事の悩み":

        reply = TextSendMessage(
        text="委員長に相談できます。\nどうしますか？",
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(
                        label="お願いします",
                        text="お願いします"
                    )
                ),
                QuickReplyButton(
                    action=MessageAction(
                        label="いいえ結構です",
                        text="いいえ結構です"
                    )
                ),
            ]
        )
    )
        line_bot_api.reply_message(
            event.reply_token,
            reply
        )
        return
    elif text == "お願いします":
        user.step = "wait_phone_number"
        user.save()

        reply = TextSendMessage(
            text="電話番号を入力してください。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )
        return


    elif user.step == "wait_phone_number":

        phone = text

        # 電話番号をLINE LOGへ保存
        LineLog.objects.create(
            user=user,
            message_type="text",
            content=f"電話番号: {phone}"
        )

        user.step = ""
        user.save()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="ありがとうございます。\n\n委員長からお電話させます。"
            )
        )
        return


    elif text == "いいえ結構です":

        user.step = ""
        user.save()

        reply = TextSendMessage(
            text=(
                "会社には内部通報がありますので\n"
                "ご利用ください。\n\n"
                "TEL 092-123-4567"
            )
        )

        line_bot_api.reply_message(
        event.reply_token,
        reply
        )
        return
    # =========================
    # 緊急生存確認
    # =========================
    
    elif text == "無事です":
        
        reply = TextSendMessage(
            text="より安全な場所へ移動してください。\n\n困っている方がいたら助け合いをお願いします。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "ケガ":

        reply = TextSendMessage(
            text="大丈夫ですか？\n\n周囲に人がいたら助けを求めてください。\n\nGPSを送信してください。"
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "危険":

        reply = TextSendMessage(
            text="近くに人はいますか？",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(
                            label="近くにいます",
                            text="近くにいます"
                        )
                    ),
                    QuickReplyButton(
                        action=MessageAction(
                            label="誰もいません",
                            text="誰もいません"
                        )
                    ),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "近くにいます":

        reply = TextSendMessage(
            text="近くの人と一緒に安全な場所へ避難してください。\n\nGPSを送信してください。"
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

    elif text == "誰もいません":

        user.step = "wait_gps"
        user.save()

        reply = TextSendMessage(
            text=(
                "落ち着いてください。\n\n"
                "こちらから救援や電話での対応ができないか確認いたします。\n\n"
                "まずGPSを送ってください。\n"
                "その後、電話番号を入力してください。\n\n"
                "【GPSの送り方】\n\n"
                "① LINEの左下にある「＋」を押します。\n"
                "② 「位置情報」を選択します。\n"
                "③ 「現在地を送信」を押してください。"
            )
)
        line_bot_api.reply_message(
            event.reply_token,
            reply
            )
        return
    elif user.step == "wait_phone_number":

    # 電話番号を保存
        user.phone = text
        user.step = ""
        user.save()

    # LINE LOGへ保存
        LineLog.objects.create(
            user=user,
            sender="USER",
            message_type="電話番号",
            content=text
            )

        reply = TextSendMessage(
        text=(
            "電話番号を確認しました。\n\n"
            "ありがとうございます。\n\n"
            "現在の状況を確認し、\n"
            "救援や電話での対応ができないか確認いたします。\n\n"
            "委員長または組合からご連絡いたしますので、\n"
            "しばらくお待ちください。"
        )
    )
        return
    else:
        reply = TextSendMessage(
        text="組合から連絡させて下さい"
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )
        return
    
    
        
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):

    user_id = event.source.user_id
    user = LineUser.objects.get(user_id=user_id)

    gps_text = (
    f"緯度: {event.message.latitude}\n"
    f"経度: {event.message.longitude}"
    )

    LineLog.objects.create(
        user=user,
        message_type="location",
        content=gps_text
    )

    # 電話番号入力待ち
    user.step = "wait_emergency_phone"
    user.save()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="ありがとうございます。\n\n続いて電話番号を入力してください。"
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        reply
        )         
    return

# -------------------------
# LINE LOG
# -------------------------
def line_logs(request):

    logs = (
        LineLog.objects
        .select_related("user")
        .order_by("-created_at")
    )

    return render(
        request,
        "checkapp/line_logs.html",
        {
            "logs": logs,
        }
    )