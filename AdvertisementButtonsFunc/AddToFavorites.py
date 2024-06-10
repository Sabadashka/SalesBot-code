from DataBase.Advertisement_database import get_all_info_about_advertisement
from DataBase.Favorites_database import is_advertisement_in_favorites, create_new_favorite


def add_to_favorites(bot, call, telegram_id, ad_id):
    info = get_all_info_about_advertisement(ad_id)
    name = info[4]
    name_markdown = f"*{name}*"
    name_menu = '*❤️ Вибрані*'

    if not is_advertisement_in_favorites(telegram_id, ad_id):
        create_new_favorite(telegram_id, ad_id)
        bot.send_message(call.message.chat.id, f"❗️ Оголошення '{name_markdown}' успішно додано до '{name_menu}'",
                         parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, f"❌ Оголошення '{name_markdown}' вже є у '{name_menu}'",
                         parse_mode='Markdown')