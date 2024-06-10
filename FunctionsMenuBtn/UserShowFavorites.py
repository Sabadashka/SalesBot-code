import os

from telebot import types

from DataBase.Advertisement_database import get_all_info_about_advertisement
from DataBase.Favorites_database import get_user_favorites, delete_advertisement_from_favorites
from Markups.menu_markups import keyboard_menu
from OtherTools.CurrencyСonverter import convert_currency
from OtherTools.MonthConverter import format_ukrainian_datetime


def show_user_favorites_with_status_published(bot, message):
    user_id = message.from_user.id
    user_favorites = get_user_favorites(user_id)

    if user_favorites:
        show_favorite_advertisement_settings = types.InlineKeyboardMarkup(row_width=1)

        text = "<b>❤️ Ваші вибрані оголошення:</b>\n\n<i> - Ви можете натиснути на оголошення в списку, щоб переглянути його</i>"

        for i, ad in enumerate(user_favorites, start=1):
            ad_id = ad[2]
            info_ad = get_all_info_about_advertisement(ad_id)
            advertisement_id = info_ad[0]
            name = info_ad[4]
            favorite_show = types.InlineKeyboardButton(f"❤️ Оголошення '{name}'", callback_data=f'show_favorite{advertisement_id}')
            show_favorite_advertisement_settings.add(favorite_show)

        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=show_favorite_advertisement_settings)
    else:
        bot.send_message(message.chat.id, "<b>💔 Ви ще не додали жодного оголошення до вибраних</b>", parse_mode='HTML')


def print_favorite(bot, message, ad_id):
    acc_id = message.chat.id
    ad_info = get_all_info_about_advertisement(ad_id)

    if ad_info:
        status = ad_info[13]

        if status == 'published':
            price_uah = ad_info[7]
            formatted_price_uah = '{:,}'.format(price_uah).replace(',', ' ')

            converted_price_usd = convert_currency(price_uah, 'UAH', 'USD')
            formatted_price_usd = '{:,}'.format(converted_price_usd).replace(',', ' ')

            formatted_date = format_ukrainian_datetime(ad_info[8])

            ad_info_message = (
                f"❤️ *{'-' * 5} Вибране {'-' * 5}* ❤️️\n\n"
                f"📝 *Назва:* {ad_info[4]}\n\n"
                f"*Категорії:* '{ad_info[2]}' *-> Підкатегорії:* '{ad_info[3]}'\n\n"
                f"*Стан:* {ad_info[15]}\n\n"
                f"💬 *Опис:* {ad_info[5]}\n\n"
                f"💰 *Ціна:* {formatted_price_uah}₴ (${formatted_price_usd})\n"
                f"🗓 *Дата публікації:* {formatted_date}\n\n"
                f"📍 *Місце знаходження:* {ad_info[11]}, {ad_info[12]}"
            )

            folder_name = ad_info[6]

            photo_file_path = os.path.join("photos", folder_name, "photo_1.jpg")

            ad_func = types.InlineKeyboardMarkup(row_width=1)
            show_all_photos_button = types.InlineKeyboardButton("📷Показати всі фото",
                                                                callback_data=f'show_all_photos_button{ad_info[0]}')
            show_contacts = types.InlineKeyboardButton("ℹ️ Зв'язатися з продавцем",
                                                       callback_data=f'show_contacts_btn{ad_info[0]}')
            add_to_favorites = types.InlineKeyboardButton("❌ Видалити з вибраних",
                                                          callback_data=f'delete_from_favorites_btn{ad_info[0]}')
            complain = types.InlineKeyboardButton("⚠️ Поскаржитись на оголошення",
                                                  callback_data=f'complain_btn{ad_info[0]}')
            ad_func.add(show_all_photos_button, show_contacts, add_to_favorites, complain)

            with open(photo_file_path, 'rb') as photo:
                bot.send_photo(acc_id, photo, caption=ad_info_message, parse_mode="Markdown", reply_markup=ad_func)

        elif status == 'on moderation':
            text = f"❤️ *Оголошення *{ad_info[4]}* знаходиться на модерації та згодом повернеться у *'❤️ Вибрані'*"
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard_menu)

        else:
            bot.send_message(message.chat.id, f"<b>❗️ Не знайдено інформації для оголошення</b>", parse_mode='HTML',
                             reply_markup=keyboard_menu)
            delete_advertisement_from_favorites(ad_id)

    else:
        bot.send_message(message.chat.id, f"<b>❗️ Не знайдено інформації для оголошення</b>", parse_mode='HTML', reply_markup=keyboard_menu)