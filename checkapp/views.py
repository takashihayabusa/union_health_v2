from django.shortcuts import render,redirect
from django.http import HttpResponse
from openpyxl import Workbook
from django.views.decorators.csrf import csrf_exempt
from openpyxl.styles import Font, PatternFill, Alignment

from linebot import LineBotApi, WebhookHandler
from linebot.models import *

from django.conf import settings
from .models import LineUser, LineLog

from openpyxl.styles import PatternFill, Font
from datetime import datetime
import re


print("CHECKAPP 起動")


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
# =====================================
# LINE LOG 共通保存
# =====================================

def save_line_log(user, sender, message_type, content):

    try:

        LineLog.objects.create(
            user=user,
            sender=sender,
            message_type=message_type,
            content=content
        )

    except Exception as e:

        print("LINE LOG 保存エラー:", e)


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

        try:
            line_bot_api.push_message(
                user_id,
                TextSendMessage(
                    text=(
                        "📢 マルキョウユニオンLINEホームページ\n\n"
                        "登録ありがとうございます。\n"
                        "マルキョウユニオンLINEホームページはこちらからご利用ください。"
                    )
                )
            )
            print("LINE送信成功")
        except Exception as e:
            print("LINE送信失敗:", e)

            return render(
                request,
                    "checkapp/register_complete.html"
                    )

    # GETのときは登録画面を表示
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
        
        user.step = ""
        user.save()

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



def clear_test_users(request):

    LineUser.objects.filter(
        user_id__startswith="web_"
    ).delete()

    return redirect("/users/")
def clear_all_users(request):

    LineUser.objects.all().delete()

    return redirect("/users/")

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
            "下記の登録ページから\n\n"
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
    print("現在のstep:", user.step)

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
        line_bot_api.reply_message(
        event.reply_token,
        reply
)

    elif text == "少し疲れています":

        reply = TextSendMessage(
            text="無理をしないでください。休息を取ってください。"
        )
        line_bot_api.reply_message(
        event.reply_token,
        reply
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

    # USERログ
        save_line_log(
            user,
            "USER",
            "電話番号",
            text
            )

        user.step = ""
        user.save()

        reply = TextSendMessage(
            text=(
                "電話番号ありがとうございました。\n\n"
                "委員長へ連絡いたします。"
            )
        )

    # BOTログ
        save_line_log(
            user,
            "BOT",
            "健康チェック",
            "電話番号ありがとうございました。委員長から連絡させます。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
        )
        return

    elif user.step == "wait_emergency_phone":

    # USERログ
        save_line_log(
            user,
            "USER",
            "緊急電話番号",
            text
            )

        user.step = ""
        user.save()

        reply = TextSendMessage(
        text=(
            "電話番号を確認しました。\n\n"
            "ありがとうございます。\n\n"
            "現在の状況を確認し、救援や電話での対応ができないか確認いたします。\n\n"
            "今の状況が変ったら下記に電話ください\n\n"
            "【委員長】\n"
            "TEL：090-XXXX-XXXX\n\n"
            "【組合】\n"
            "TEL：092-XXX-XXXX\n\n"
            )
        )

    # BOTログ
        save_line_log(
            user,
            "BOT",
            "緊急",
            "電話番号を確認しました。現在の状況を確認し、救援や電話での対応ができないか確認いたします。委員長または組合からご連絡いたしますので、しばらくお待ちください。状況が変わった場合や、安全な場所へ避難できた場合は、そのままLINEでお知らせください。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
            )
        return

    # 電話番号を保存
    # USERログ
        save_line_log( 
            user,
            "USER",
            "電話番号",
            text
            )

        reply = TextSendMessage(
            text=(
                "電話番号を確認しました。\n\n"
                "ありがとうございます。\n\n"
                "委員長または組合からご連絡いたしますので、\n"
                "しばらくお待ちください。"
            )
)

    # BOTログ
        save_line_log(
            user,
            "BOT",
            "電話番号",
            "電話番号を確認しました。委員長または組合からご連絡いたしますので、しばらくお待ちください。"
)

        line_bot_api.reply_message(
            event.reply_token,
            reply
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

    # USERのメッセージを保存
        save_line_log(
            user,
            "USER",
            "緊急",
            text
            )

        reply = TextSendMessage(
            text=(
                "より安全な場所へ移動してください。\n\n"
                "困っている方がいたら助け合いをお願いします。"
                "こちらとしても安心しますのでGPSを送って下さい"
                "【GPSの送り方】\n\n"
                "① LINEの左下にある「＋」を押します。\n"
                "② 「位置情報」を選択します。\n"
                "③ 「現在地を送信」を押してください。"
                )
            )

    # BOTの返信を保存
        save_line_log(
            user,
            "BOT",
            "緊急",
            "より安全な場所へ移動してください。困っている方がいたら助け合いをお願いします。"
            "こちらとしても安心しますのでGPSを送って下さい"
            "【GPSの送り方】\n\n"
                "① LINEの左下にある「＋」を押します。\n"
                "② 「位置情報」を選択します。\n"
                "③ 「現在地を送信」を押してください。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
            )
    elif text == "ケガ":

    # USERログ
        save_line_log(
            user,
            "USER",
            "緊急",
            text
            )

        user.step = "wait_gps"
        user.save()

        reply = TextSendMessage(
            text=(
                "ケガをされているとのことですね。\n\n"
                "誰か周りにいたら助けを求めて下さい\n\n"
                "救援や電話での対応ができないか確認いたします。\n\n"
                "まずGPSを送信してください。\n\n"
                "【GPSの送り方】\n\n"
                "① LINEの左下にある「＋」を押します。\n"
                "② 「位置情報」を選択します。\n"
                "③ 「現在地を送信」を押してください。"
                "今の状況が変ったら下記に電話ください\n\n"
                "【委員長】\n"
                "TEL：090-XXXX-XXXX\n\n"
                "【組合】\n"
                "TEL：092-XXX-XXXX\n\n"
                
                
                )
            )

    # BOTログ
        save_line_log(
            user,
            "BOT",
            "緊急",
            "ケガをされているとのことですね。まず安全を確保してください。GPSを送信してください。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
            )
        return

    elif text == "危険":

        
        save_line_log(
            user,
            "USER",
            "緊急",
            text
            )

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
            # BOTログ
        save_line_log(
            user,
            "BOT",
            "緊急",
            "近くに人はいますか？"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
            )


    elif text == "近くにいます":

    # USERログ

        save_line_log(
            user,
            "USER",
            "緊急",
            text
            )

        reply = TextSendMessage(
            text="近くの人と一緒に安全な場所へ避難してください。\n\n"
            "【GPSの送り方】\n\n"
                "① LINEの左下にある「＋」を押します。\n"
                "② 「位置情報」を選択します。\n"
                "③ 「現在地を送信」を押してください。"
            )

        save_line_log(
            user,
            "BOT",
            "緊急",
            "近くの人と一緒に安全な場所へ避難してください。"
            "こちらとして安心しますのでGPSを送って下さい"
            "【GPSの送り方】\n\n"
                "① LINEの左下にある「＋」を押します。\n"
                "② 「位置情報」を選択します。\n"
                "③ 「現在地を送信」を押してください。"
            )

        line_bot_api.reply_message(
            event.reply_token,
            reply
            )


    elif text == "誰もいません":

    # USERログ
        save_line_log(
            user,
            "USER",
            "緊急",
            text
            )

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

    # BOTログ

        save_line_log(
            user,
            "BOT",
            "緊急",
            "落ち着いてください。こちらから救援や電話での対応ができないか確認いたします。まずGPSを送ってください。その後、電話番号を入力してください。"
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


def export_logs_excel(request):

    wb = Workbook()
    red_fill = PatternFill(
        fill_type="solid",
        fgColor="FF0000"
    )

    blue_fill = PatternFill(
        fill_type="solid",
        fgColor="0066CC"
    )

    white_font = Font(
        color="FFFFFF",
        bold=True
    )

    ws = wb.active

    ws.title = "LINE LOG"


    # 見出し
    ws.append([
        "日時",
        "名前",
        "地域",
        "送信者",
        "種類",
        "内容"
    ])

    # 見出しを赤にする
    for cell in ws[1]:
        cell.fill = red_fill
        cell.font = white_font
    # LINE LOG を取得
    logs = LineLog.objects.select_related("user").order_by("created_at")

    for log in logs:

        ws.append([
            log.created_at.strftime("%Y-%m-%d %H:%M"),
            log.user.name,
            log.user.region,
            log.sender,
            log.message_type,
            log.content
            ])
        print(log.message_type)
        current_row = ws.max_row
        
        content = str(ws.cell(row=current_row, column=6).value)

        # 危険
        if "危険" in content:

            for col in range(1, 7):
                cell = ws.cell(row=current_row, column=col)
                cell.fill = red_fill
                cell.font = white_font

        # ケガ
        elif "ケガ" in content:

            orange_fill = PatternFill(
                fill_type="solid",
                fgColor="FFA500"
            )

            for col in range(1, 7):
                cell = ws.cell(row=current_row, column=col)
                cell.fill = orange_fill

        # 電話番号
        elif content.isdigit() and len(content) >= 10:

            for col in range(1, 7):
                cell = ws.cell(row=current_row, column=col)
                cell.fill = blue_fill
                cell.font = white_font

        # GPS
        # GPS
        elif log.message_type in ["GPS", "location"]:

                gps_fill = PatternFill(
                fill_type="solid",
                fgColor="CCFFFF"
                )

                for col in range(1, 7):
                    cell = ws.cell(row=current_row, column=col)
                    cell.fill = gps_fill


    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="LINE_LOG.xlsx"'
    )

    wb.save(response)

    return response

def delete_logs(request):

    LineLog.objects.all().delete()

    return redirect("line_logs")