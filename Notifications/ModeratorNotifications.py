import settings


def notification_new_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Нове оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Нове оголошення</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_activation_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Активація оголошення</b>"
    )
    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_new_description_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Зміна опису оголошення</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_new_photos_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Оновлення фотографій оголошення</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_new_location_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Зміна місцезнаходжуння оголошення</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_extend_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Продовження терміну оголошення на 30 днів</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_new_name_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Зміна назви оголошення</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_new_price_ad(bot, name, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Оголошення <b>'{name}'</b> очікує на перевірку!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
        f"❗️ <b>Зміна ціни оголошення</b>"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')


def notification_new_question(bot, owner_id):
    group_chat_id = settings.group_chat_id
    message_text = (
        f"❗️ <b>[MODERATOR]</b> Нове запитання!\n"
        f"👤 Користувач ID: <code>{owner_id}</code>\n"
    )

    bot.send_message(group_chat_id, text=message_text, parse_mode='HTML')
