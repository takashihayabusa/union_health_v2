# =====================================
# 健康チェック開始
# =====================================

elif user.step == "health_start":

    # -----------------------------
    # 元気
    # -----------------------------

    if "元気" in text:

        user.step = "healthy_good"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(

                text=(
                    "よかったです。\n\n"
                    "無理をしないでください。\n\n"
                    "しっかり睡眠を取ってください。"
                ),

                quick_reply=QuickReply(
                    items=[

                        QuickReplyButton(
                            action=MessageAction(
                                label="ありがとうございます",
                                text="ありがとうございます"
                            )
                        ),

                    ]
                )
            )
        )

# =====================================
# 元気終了
# =====================================

elif user.step == "healthy_good":

    user.step = "done"
    user.save()

    line_bot_api.reply_message(

        event.reply_token,

        TextSendMessage(
            text="今日も安全第一でお願いします。"
        )
    )

# =====================================
# 少し疲れ
# =====================================

elif user.step == "health_tired":

    user.step = "health_tired_2"
    user.save()

    line_bot_api.reply_message(

        event.reply_token,

        TextSendMessage(

            text=(
                "無理をしないでください。\n"
                "休息を取ってください。\n\n"
                "食事や睡眠は取れていますか？"
            ),

            quick_reply=QuickReply(
                items=[

                    QuickReplyButton(
                        action=MessageAction(
                            label="取れています",
                            text="取れています"
                        )
                    ),

                    QuickReplyButton(
                        action=MessageAction(
                            label="取れていません",
                            text="取れていません"
                        )
                    ),

                ]
            )
        )
    )

# =====================================
# 少し疲れ２
# =====================================

elif user.step == "health_tired_2":

    # -----------------------------
    # 取れている
    # -----------------------------

    if "取れています" in text:

        user.step = "done"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "安心しました。\n\n"
                    "つらい時は\n"
                    "いつでも相談してください。"
                )
            )
        )

    # -----------------------------
    # 取れていない
    # -----------------------------

    elif "取れていません" in text:

        user.step = "health_tired_3"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(

                text=(
                    "かなり疲れが溜まっている可能性があります。\n\n"
                    "相談しますか？"
                ),

                quick_reply=QuickReply(
                    items=[

                        QuickReplyButton(
                            action=MessageAction(
                                label="相談する",
                                text="相談する"
                            )
                        ),

                        QuickReplyButton(
                            action=MessageAction(
                                label="まだ大丈夫",
                                text="まだ大丈夫"
                            )
                        ),

                    ]
                )
            )
        )

# =====================================
# 少し疲れ３
# =====================================

elif user.step == "health_tired_3":

    # -----------------------------
    # 相談する
    # -----------------------------

    if "相談" in text:

        user.step = "done"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "無理をしないでください。\n\n"
                    "必要であれば\n"
                    "組合へ相談してください。"
                )
            )
        )

    # -----------------------------
    # まだ大丈夫
    # -----------------------------

    else:

        user.step = "done"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "無理をしすぎないでください。\n\n"
                    "つらい時は\n"
                    "いつでも相談してください。"
                )
            )
        )

# =====================================
# かなり辛い
# =====================================

elif user.step == "health_hard":

    # -----------------------------
    # 体
    # -----------------------------

    if "体" in text:

        user.step = "body_hard"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(

                text=(
                    "病院受診をおすすめします。\n\n"
                    "食事や睡眠は取れていますか？"
                ),

                quick_reply=QuickReply(
                    items=[

                        QuickReplyButton(
                            action=MessageAction(
                                label="取れています",
                                text="取れています"
                            )
                        ),

                        QuickReplyButton(
                            action=MessageAction(
                                label="取れていません",
                                text="取れていません"
                            )
                        ),

                    ]
                )
            )
        )

    # -----------------------------
    # メンタル
    # -----------------------------

    elif "メンタル" in text:

        user.step = "mental_reason"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(

                text=(
                    "個人の問題ですか？\n"
                    "会社が原因ですか？"
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
        )

# =====================================
# 身体的につらい
# =====================================

elif user.step == "body_hard":

    user.step = "done"
    user.save()

    # -----------------------------
    # 取れていない
    # -----------------------------

    if "取れていません" in text:

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "かなり危険な状態の可能性があります。\n\n"
                    "病院受診や休養をおすすめします。"
                )
            )
        )

    # -----------------------------
    # 取れている
    # -----------------------------

    else:

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "無理をしないでください。\n\n"
                    "症状が続く場合は\n"
                    "病院受診をおすすめします。"
                )
            )
        )

# =====================================
# メンタル原因
# =====================================

elif user.step == "mental_reason":

    # -----------------------------
    # 個人
    # -----------------------------

    if "個人" in text:

        user.step = "done"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "一人で抱え込まないようにしてください。\n\n"
                    "信頼できる身近な方へ\n"
                    "相談してください。"
                )
            )
        )

    # -----------------------------
    # 会社
    # -----------------------------

    elif "会社" in text:

        user.step = "mental_support"
        user.save()

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(

                text=(
                    "組合の委員長が\n"
                    "相談に乗ります。"
                ),

                quick_reply=QuickReply(
                    items=[

                        QuickReplyButton(
                            action=MessageAction(
                                label="電話",
                                text="電話"
                            )
                        ),

                        QuickReplyButton(
                            action=MessageAction(
                                label="LINE",
                                text="LINE"
                            )
                        ),

                        QuickReplyButton(
                            action=MessageAction(
                                label="まだ大丈夫",
                                text="まだ大丈夫"
                            )
                        ),

                    ]
                )
            )
        )

# =====================================
# メンタル相談
# =====================================

elif user.step == "mental_support":

    user.step = "done"
    user.save()

    # -----------------------------
    # 電話
    # -----------------------------

    if "電話" in text:

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "組合委員長へ電話してください。\n\n"
                    "TEL:\n"
                    "090-XXXX-XXXX"
                )
            )
        )

    # -----------------------------
    # LINE
    # -----------------------------

    elif "LINE" in text:

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "委員長へLINEで\n"
                    "相談してください。\n\n"
                    "状況を簡単に送るだけでも\n"
                    "大丈夫です。"
                )
            )
        )

    # -----------------------------
    # まだ大丈夫
    # -----------------------------

    else:

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(
                text=(
                    "無理をしすぎないでください。\n\n"
                    "信頼できる身近な方へ\n"
                    "相談してください。"
                )
            )
        )