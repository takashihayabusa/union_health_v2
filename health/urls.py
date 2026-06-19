from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FollowEvent,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
)

from .models import LineUser


# LINE設定
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):

    if request.method != "POST":
        return HttpResponse("OK")

    signature = request.META["HTTP_X_LINE_SIGNATURE"]

    body = request.body.decode("utf-8")

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        return HttpResponse("Invalid signature", status=400)

    return HttpResponse("OK")


# 友だち追加時
@handler.add(FollowEvent)
def handle_follow(event):

    user_id = event.source.user_id

    LineUser.objects.get_or_create(
        user_id=user_id
    )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="登録しました。\nお名前を入力してください。"
        )
    )


# メッセージ受信
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id
    text = event.message.text

    # ユーザー取得
    user, created = LineUser.objects.get_or_create(
        user_id=user_id
    )

    # 名前未登録
    if not user.name:

        user.name = text
        user.save()

        buttons_template = TemplateSendMessage(
            alt_text='地域登録',
            template=ButtonsTemplate(
                title='地域登録',
                text='地域を選択してください',
                actions=[
                    MessageAction(label='福岡', text='福岡'),
                    MessageAction(label='佐賀', text='佐賀'),
                    MessageAction(label='長崎', text='長崎'),
                    MessageAction(label='熊本', text='熊本'),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            buttons_template
        )

        return

    # 地域登録
    if text in ['福岡', '佐賀', '長崎', '熊本']:

        user.region = text
        user.save()

        buttons_template = TemplateSendMessage(
            alt_text='健康チェック',
            template=ButtonsTemplate(
                title='健康チェック',
                text='現在の体調を選択してください',
                actions=[
                    MessageAction(label='元気', text='元気'),
                    MessageAction(label='少し疲れ', text='少し疲れ'),
                    MessageAction(label='かなり悪い', text='かなり悪い'),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=f'{user.name}さん（{user.region}）登録完了しました。'
                ),
                buttons_template
            ]
        )

        return

    # 元気
    if text == "元気":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="安心しました。今日も無理をしすぎないでください。"
            )
        )

        return

    # 少し疲れ
    elif text == "少し疲れ":

        buttons_template = TemplateSendMessage(
            alt_text='少し疲れ',
            template=ButtonsTemplate(
                title='少し疲れ',
                text='大丈夫でしょうか？\n無理をしないでください。\nもし休めるなら休んでください。',
                actions=[
                    MessageAction(label='はい', text='はい'),
                    MessageAction(label='いいえ', text='いいえ'),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            buttons_template
        )

        return

    # かなり悪い
    elif text == "かなり悪い":

        buttons_template = TemplateSendMessage(
            alt_text='かなり悪い',
            template=ButtonsTemplate(
                title='かなり悪い',
                text='体調ですか？\nメンタルですか？',
                actions=[
                    MessageAction(label='体調', text='体調'),
                    MessageAction(label='メンタル', text='メンタル'),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            buttons_template
        )

        return

    # 体調
    elif text == "体調":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='無理をせずに病院に行って下さい。'
            )
        )

        return

    # メンタル
    elif text == "メンタル":

        buttons_template = TemplateSendMessage(
            alt_text='メンタル',
            template=ButtonsTemplate(
                title='メンタル',
                text='個人の事ですか？\n仕事の事ですか？',
                actions=[
                    MessageAction(label='個人の事', text='個人の事'),
                    MessageAction(label='仕事の事', text='仕事の事'),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            buttons_template
        )

        return

    # 個人の事
    elif text == "個人の事":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='誰か信用できる方に相談して下さい。\n自分で溜め込まないようにして下さい。'
            )
        )

        return

    # 仕事の事
    elif text == "仕事の事":

        buttons_template = TemplateSendMessage(
            alt_text='仕事の事',
            template=ButtonsTemplate(
                title='仕事の事',
                text='組合の委員長が相談にのります。',
                actions=[
                    MessageAction(label='電話しますか', text='電話'),
                    MessageAction(label='LINEで相談しますか', text='LINE相談'),
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            buttons_template
        )

        return

    # 電話
    elif text == "電話":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='委員長へ電話してください。'
            )
        )

        return

    # LINE相談
    elif text == "LINE相談":

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='LINEで相談内容を送信してください。'
            )
        )

        return

    # その他
    else:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='健康チェックありがとうございます。'
            )
        )