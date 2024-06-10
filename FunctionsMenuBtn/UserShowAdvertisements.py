import os
from telebot.types import Message
from DataBase.Advertisement_database import get_user_advertisements_with_status_published, \
    get_user_advertisements_with_status_on_moderation, get_user_advertisements_with_status_deleted, \
    get_user_advertisements_with_status_deactivated, get_all_info_about_advertisement
from telebot import TeleBot, types

from DataBase.Notified_database import get_notified_id, get_notified_user
from Markups.menu_markups import markup_ad_types
from OtherTools.CurrencyСonverter import convert_currency
from OtherTools.MonthConverter import format_ukrainian_datetime


def request_ad_type(bot, message):
    bot.send_message(message.chat.id, "<b>❗️️ Оберіть тип оголошень для перегляду</b>", parse_mode='HTML',
                     reply_markup=markup_ad_types)


def show_user_advertisements_with_status_published(bot: TeleBot, message: Message):
    user_id = message.from_user.id
    user_advertisements = get_user_advertisements_with_status_published(user_id)

    if user_advertisements:
        advertisement_show_settings = types.InlineKeyboardMarkup(row_width=1)

        text = "<b>⚠️ Активні оголошення:</b>\n\n<i> - Ви можете натиснути на оголошення в списку, щоб переглянути його</i>"

        for i, ad in enumerate(user_advertisements, start=1):
            name = ad[4]
            advertisement_show = types.InlineKeyboardButton(f"{name}", callback_data=f'show_advertisement{ad[0]}')
            advertisement_show_settings.add(advertisement_show)

        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=advertisement_show_settings)
    else:
        bot.send_message(message.chat.id, "<b>🤷‍♂️ У Вас немає активних оголошень</b>", parse_mode='HTML')


def show_user_advertisements_with_status_on_moderation(bot: TeleBot, message: Message):
    user_id = message.from_user.id
    user_advertisements = get_user_advertisements_with_status_on_moderation(user_id)

    if user_advertisements:
        advertisement_show_settings = types.InlineKeyboardMarkup(row_width=1)

        text = "<b>⚠️ Оголошення, що очікують на перевірку:</b>\n\n<i> - Ви можете натиснути на оголошення в списку, щоб переглянути його</i>"

        for ad in user_advertisements:
            name = ad[4]
            advertisement_show = types.InlineKeyboardButton(f"{name}", callback_data=f'show_advertisement{ad[0]}')
            advertisement_show_settings.add(advertisement_show)

        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=advertisement_show_settings)

    else:
        bot.send_message(message.chat.id, "🤷‍♂️ <b>У Вас немає оголошень, які очікують перевірку</b>",
                         parse_mode='HTML')


def show_user_advertisements_with_status_deactivated(bot: TeleBot, message: Message):
    user_id = message.from_user.id
    user_advertisements = get_user_advertisements_with_status_deactivated(user_id)

    if user_advertisements:
        advertisement_show_settings = types.InlineKeyboardMarkup(row_width=1)

        text = "<b>⚠️ Деактивовані оголошення:</b>\n\n<i> - Ви можете натиснути на оголошення в списку, щоб переглянути його</i>"

        for ad in user_advertisements:
            name = ad[4]
            advertisement_show = types.InlineKeyboardButton(f"{name}", callback_data=f'show_advertisement{ad[0]}')
            advertisement_show_settings.add(advertisement_show)

        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=advertisement_show_settings)
    else:
        bot.send_message(message.chat.id, "🤷‍♂️ <b>Ви не видаляли жодного оголошення</b>", parse_mode='HTML')


def show_user_advertisements_with_status_deleted(bot: TeleBot, message: Message):
    user_id = message.from_user.id
    user_advertisements = get_user_advertisements_with_status_deleted(user_id)

    if user_advertisements:
        advertisement_show_settings = types.InlineKeyboardMarkup(row_width=1)

        text = "<b>⚠️ Видалені оголошення:</b>\n\n<i> - Ви можете натиснути на оголошення в списку, щоб переглянути його</i>"

        for ad in user_advertisements:
            name = ad[4]
            advertisement_show = types.InlineKeyboardButton(f"{name}", callback_data=f'show_advertisement{ad[0]}')
            advertisement_show_settings.add(advertisement_show)

        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=advertisement_show_settings)
    else:
        bot.send_message(message.chat.id, "🤷‍♂️ <b>Ви не видаляли жодного оголошення</b>", parse_mode='HTML')


def send_advertisement(bot, message, ad_id):
    ad_info = get_all_info_about_advertisement(ad_id)
    status = ad_info[13]
    advertisement_id = ad_info[0]
    telegram_id = ad_info[1]
    price_uah = ad_info[7]
    formatted_price_uah = '{:,}'.format(price_uah).replace(',', ' ')
    converted_price_usd = convert_currency(price_uah, 'UAH', 'USD')
    formatted_price_usd = '{:,}'.format(converted_price_usd).replace(',', ' ')
    formatted_date = format_ukrainian_datetime(ad_info[8])

    if status == 'on moderation':
        status_text = 'Оголошення знаходиться на модерації'
    elif status == 'deactivated':
        status_text = 'Оголошення деактивовано'
    elif status == 'deleted':
        status_text = 'Оголошення видалено'
    else:
        status_text = 'Оголошення опубліковане'

    adv_info = (
        # f"⭐️ *{'-' * 5} Оголошення {'-' * 5}* ⭐️\n\n"
        f"📝 *Назва:* {ad_info[4]}\n\n"
        f"*Категорії:* '{ad_info[2]}' *-> Підкатегорії:* '{ad_info[3]}'\n\n"
        f"*Стан:* {ad_info[15]}\n\n"
        f"💬 *Опис:* {ad_info[5]}\n\n"
        f"💰 *Ціна:* {formatted_price_uah}₴ (${formatted_price_usd})\n"
        f"🗓 *Дата публікації:* {formatted_date}\n\n"
        f"📍 *Місце знаходження:* {ad_info[11]}, {ad_info[12]}\n\n"
        f"❗️️ *Статус оголошення:* {status_text}"
    )

    folder_name = ad_info[6]
    photo_file_path = os.path.join("photos", folder_name, "photo_1.jpg")

    ad_settings = types.InlineKeyboardMarkup(row_width=1)

    if status == 'on moderation':
        show_all_photos_button = types.InlineKeyboardButton("📷Показати всі фото",
                                                            callback_data=f'show_all_photos_button{ad_info[0]}')
        delete_button = types.InlineKeyboardButton("❌ Видалити оголошення", callback_data=f'delete_ad{ad_info[0]}')
        ad_settings.add(show_all_photos_button, delete_button)
    elif status == 'deactivated':
        show_all_photos_button = types.InlineKeyboardButton("📷Показати всі фото",
                                                            callback_data=f'show_all_photos_button{ad_info[0]}')
        activate_button = types.InlineKeyboardButton("🔄 Активувати оголошення",
                                                     callback_data=f'activate_ad{ad_info[0]}')
        delete_button = types.InlineKeyboardButton("❌ Видалити оголошення", callback_data=f'delete_ad{ad_info[0]}')
        ad_settings.add(show_all_photos_button, activate_button, delete_button)
    elif status == 'deleted':
        pass
    else:
        show_all_photos_button = types.InlineKeyboardButton("📷Показати всі фото",
                                                            callback_data=f'show_all_photos_button{ad_info[0]}')
        deactivate_button = types.InlineKeyboardButton("✅ Позначити як продано",
                                                       callback_data=f'deactivate_ad{ad_info[0]}')
        edit_button = types.InlineKeyboardButton("🛠 Редагувати оголошення", callback_data=f'edit_ad{ad_info[0]}')
        delete_button = types.InlineKeyboardButton("❌ Видалити оголошення", callback_data=f'delete_ad{ad_info[0]}')
        notified_id = get_notified_user(telegram_id, advertisement_id)
        if notified_id:
            extend_button = types.InlineKeyboardButton("🔄 Продовжити оголошення",
                                                       callback_data=f'extend_ad{ad_info[0]}')
            ad_settings.add(show_all_photos_button, deactivate_button, edit_button, delete_button, extend_button)
        else:
            ad_settings.add(show_all_photos_button, deactivate_button, edit_button, delete_button)

    with open(photo_file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=adv_info, parse_mode="Markdown", reply_markup=ad_settings)

