import os

from telebot import types

from DataBase.Advertisement_database import get_all_info_about_advertisement, get_info_for_moderation, \
    set_status_for_ad_on_review, get_ads_where_moderation_on_review
from DataBase.Complaints_database import get_complaints_with_status_none, set_status_for_ad_without_violation
from DataBase.Users_database import get_user_data
from Markups.menu_markups import admin_next_complaint, admin_keyboard_menu, admin_menu_keyboard_menu, \
    moderator_moderation_exit, moderator_menu_keyboard_menu, keyboard_menu
from OtherTools.CurrencyСonverter import convert_currency
from OtherTools.MonthConverter import format_ukrainian_datetime


def check_moderation(bot, message):
    acc_id = message.chat.id
    moderation_data = get_info_for_moderation(acc_id)
    user_data = get_user_data(acc_id)


    if not moderation_data:
        role = user_data.get('role', 2)
        if role == 1:
            bot.send_message(message.chat.id, "❗️ Нові оголошення відсутні", reply_markup=moderator_menu_keyboard_menu)
            return

        elif role == 2:
            bot.send_message(message.chat.id, "❗️ Нові оголошення відсутні", reply_markup=admin_menu_keyboard_menu)
            return

        else:
            bot.send_message(message.chat.id, "❗️ У Вас немає таких прав", reply_markup=keyboard_menu)
            return

    for idx, moderation in enumerate(moderation_data, start=1):
        bot.send_message(message.chat.id, "⚠️ Не затягуйте з переглядом оголошень", reply_markup=moderator_moderation_exit)

        new_status = f'on review {acc_id}'
        set_status_for_ad_on_review(moderation[0], new_status)

        ad_info = get_all_info_about_advertisement(moderation[0])

        price_uah = ad_info[7]
        formatted_price_uah = '{:,}'.format(price_uah).replace(',', ' ')

        converted_price_usd = convert_currency(price_uah, 'UAH', 'USD')
        formatted_price_usd = '{:,}'.format(converted_price_usd).replace(',', ' ')

        formatted_date = format_ukrainian_datetime(ad_info[8])

        if ad_info:
            ad_info_message = (
                f"⚠️ *На модерації № {ad_info[0]}* ️\n"
                #f"❤️ *{moderation[0]}️*\n\n"
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

            moderation_ad_func = types.InlineKeyboardMarkup(row_width=2)
            moderation_change_name_ad = types.InlineKeyboardButton("✏️ Змінити назву",
                                                                   callback_data=f'moderator_name_btn{ad_info[0]}')
            moderation_change_category_ad = types.InlineKeyboardButton("📚 Змінити категорії",
                                                                       callback_data=f'moderator_category_btn{ad_info[0]}')
            moderation_change_description_ad = types.InlineKeyboardButton("📝 Змінити опис",
                                                                          callback_data=f'moderator_description_btn{ad_info[0]}')
            show_all_photos_button = types.InlineKeyboardButton("📷Показати всі фото",
                                                                callback_data=f'show_all_photos_button{ad_info[0]}')

            moderation_publish_ad = types.InlineKeyboardButton("✅ Опублікувати",
                                                               callback_data=f'moderator_publish_ad_btn{ad_info[0]}')
            moderation_delete_ad = types.InlineKeyboardButton("🗑️ Видалити",
                                                              callback_data=f'moderator_delete_ad_btn{ad_info[0]}')
            moderation_ad_func.add(moderation_change_name_ad)
            moderation_ad_func.add(moderation_change_category_ad)
            moderation_ad_func.add(moderation_change_description_ad)
            moderation_ad_func.add(show_all_photos_button)
            moderation_ad_func.add(moderation_publish_ad, moderation_delete_ad)

            text = f'❗️ Останні зміни оголошення ID:*{ad_info[0]}*\n\n{ad_info[14]}'
            bot.send_message(acc_id, text, parse_mode="Markdown")

            with open(photo_file_path, 'rb') as photo:
                bot.send_photo(acc_id, photo, caption=ad_info_message, parse_mode="Markdown",
                               reply_markup=moderation_ad_func)

            break

        else:
            bot.send_message(message.chat.id, f"Не знайдено інформації для оголошення {ad_info[2]}.")