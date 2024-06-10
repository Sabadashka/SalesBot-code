from DataBase.Advertisement_database import get_all_info_about_advertisement
from DataBase.Favorites_database import delete_advertisement_from_favorites, \
    is_advertisement_in_favorites


def delete_favorite(bot, call, ad_id):
    telegram_id = call.from_user.id
    info = get_all_info_about_advertisement(ad_id)
    name = info[4]
    name_markdown = f"*{name}*"

    if is_advertisement_in_favorites(telegram_id, ad_id):
        delete_advertisement_from_favorites(ad_id)

        message_id = call.message.message_id
        name_menu = '*❤️ Вибрані*'
        bot.send_message(call.message.chat.id,
                         f"❗️ Оголошення '{name_markdown}' було успішно видалено з '{name_menu}'",
                         parse_mode="Markdown")

        bot.delete_message(call.message.chat.id, message_id)
    else:
        bot.send_message(call.message.chat.id,
                         f"❌ Оголошення '{name_markdown}' не знаходиться в вашому списку вибраних.",
                         parse_mode="Markdown")