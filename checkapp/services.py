from linebot.models import (
    TextSendMessage,
    QuickReply,
    QuickReplyButton,
    MessageAction,
)

from .models import LineUser
from .line_api import line_bot_api


def send_health_check_to_all():

    users = LineUser.objects.all()

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

    success = 0
    error = 0

    for user in users:

        user.step = "health_start"
        user.save()

        try:

            line_bot_api.push_message(
                user.user_id,
                message
            )

            success += 1

        except Exception as e:

            print(e)

            error += 1

    return success, error