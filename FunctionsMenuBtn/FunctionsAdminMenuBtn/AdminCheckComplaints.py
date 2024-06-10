import os

from telebot import types

from DataBase.Advertisement_database import get_all_info_about_advertisement
from DataBase.Complaints_database import get_complaints_with_status_none, set_status_for_ad_without_violation, \
    get_complaints_where_admin_on_review
from Markups.menu_markups import admin_next_complaint, admin_keyboard_menu, admin_menu_keyboard_menu, \
    admin_complaint_exit, keyboard_menu
from OtherTools.CurrencyСonverter import convert_currency
from OtherTools.MonthConverter import format_ukrainian_datetime


def check_complaints(bot, message):
    acc_id = message.chat.id
    complaints_data = get_complaints_with_status_none(acc_id)

    if not complaints_data:
        bot.send_message(message.chat.id, "❗️ Нові скарги відсутні", reply_markup=admin_menu_keyboard_menu)
        return

    for idx, complaint in enumerate(complaints_data, start=1):
        bot.send_message(message.chat.id, "⚠️ Не затягуйте зі скаргами", reply_markup=admin_complaint_exit)

        new_status = f'on review {acc_id}'
        set_status_for_ad_without_violation(complaint[0], new_status)
        ad_info = get_all_info_about_advertisement(complaint[2])

        price_uah = ad_info[7]
        formatted_price_uah = '{:,}'.format(price_uah).replace(',', ' ')

        converted_price_usd = convert_currency(price_uah, 'UAH', 'USD')
        formatted_price_usd = '{:,}'.format(converted_price_usd).replace(',', ' ')

        formatted_date = format_ukrainian_datetime(ad_info[8])

        if ad_info:
            ad_info_message = (
                f"⚠️ *{'-' * 5} Скарга №{idx} {'-' * 5}* ⚠️️\n"
                f"❤️ *{complaint[0]}️*\n\n"
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

            admin_ad_func = types.InlineKeyboardMarkup(row_width=2)
            detected_violation = types.InlineKeyboardButton("❌ Порушення/Видалити",
                                                           callback_data=f'yes_violation_btn{complaint[0]}')
            missing_violation = types.InlineKeyboardButton("✅ Порушень немає",
                                                           callback_data=f'no_violation_btn{complaint[0]}')
            show_all_photos_button = types.InlineKeyboardButton("📷Показати всі фото",
                                                                callback_data=f'show_all_photos_button{ad_info[0]}')
            admin_ad_func.add(show_all_photos_button)
            admin_ad_func.add(missing_violation, detected_violation)

            with open(photo_file_path, 'rb') as photo:
                bot.send_photo(acc_id, photo, caption=ad_info_message, parse_mode="Markdown",
                               reply_markup=admin_ad_func)

            break

        else:
            bot.send_message(message.chat.id, f"Не знайдено інформації для оголошення {complaint[2]}.")