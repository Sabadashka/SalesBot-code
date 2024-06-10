import settings


def notification_complaint(bot, telegram_id, name):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[ADMIN]</b> Нова скарга на оголошення <b>'{name}'</b>. Потрібна перевірка!\n"
        f"👤 Користувач ID: <code>{telegram_id}</code>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')