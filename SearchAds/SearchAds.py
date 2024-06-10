import os
import random
import re
import sqlite3

from telebot import types

from DataBase.Advertisement_database import get_all_info_about_advertisement
from Markups.menu_markups import ad_steps_keyboard, keyboard_menu
from OtherTools.CurrencyСonverter import convert_currency
from OtherTools.MonthConverter import format_ukrainian_datetime


class SearchAdsByBot:
    def __init__(self):
        self.matches_text = ""  # Текст збігів
        self.condition = ""  # Стан
        self.category = ""  # Категорія
        self.subcategory = ""  # Підкатегорія
        self.price_min = 0  # Ціна від
        self.price_max = float('inf')  # Ціна до
        self.location_region = ""  # Місцезнаходження
        self.location_city = ""  # Місцезнаходження
        self.sort_date = ""
        self.sort_price = ""

        self.filtered_ads = []
        self.current_index = 0  # Поточний індекс оголошення

    def clear_init(self):
        self.matches_text = ""
        self.condition = ""
        self.category = ""
        self.subcategory = ""
        self.price_min = 0
        self.price_max = float('inf')
        self.location_region = ""
        self.location_city = ""
        self.sort_date = ""
        self.sort_price = ""

    def clear_matches_text(self):
        self.matches_text = ""

    def clear_condition(self):
        self.condition = ""

    def clear_category(self):
        self.category = ""

    def clear_subcategory(self):
        self.subcategory = ""

    def clear_price_min(self):
        self.price_min = 0

    def clear_price_max(self):
        self.price_max = float('inf')

    def clear_location_region(self):
        self.location_region = ""

    def clear_location_city(self):
        self.location_city = ""

    def clear_sort_date(self):
        self.sort_date = ""

    def clear_sort_price(self):
        self.sort_price = ""

    def clear_all(self):
        self.current_index = 0
        self.filtered_ads = []

    def clear_index(self):
        self.current_index = 0

    def set_text(self, text):  # Метод для встановлення тексту збігів.
        self.matches_text = text

    def set_state(self, condition):  # Метод для встановлення стану.
        self.condition = condition

    def set_category(self, category):  # Метод для встановлення категорії.
        self.category = category

    def set_subcategory(self, subcategory):  # Метод для встановлення підкатегорії.
        self.subcategory = subcategory

    def set_price_range(self, min_price, max_price):  # Метод для встановлення діапазону цін
        self.price_min = min_price
        self.price_max = max_price

    def set_location_region(self, location_region):  # Метод для встановлення місцезнаходження location_region
        self.location_region = location_region

    def set_location_city(self, location_city):  # Метод для встановлення місцезнаходження set_location_city
        self.location_city = location_city

    def set_sort_by_date(self, sort_date):
        self.sort_date = sort_date

    def set_sort_by_price(self, sort_price):
        self.sort_price = sort_price

    def get_matches_text(self):
        return self.matches_text

    def search_ads(self):
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        query = "SELECT advertisement_id FROM advertisements WHERE advertisement_status = 'published'"

        conditions = []
        params = []

        if self.condition:
            conditions.append(f'advertisement_condition = "{self.condition}"')
        if self.category:
            conditions.append(f'advertisement_category = "{self.category}"')
        if self.subcategory:
            conditions.append(f"advertisement_subcategory = '{self.subcategory}'")
        if self.price_min:
            conditions.append(f"advertisement_price >= {self.price_min}")
        if self.price_max != float('inf'):
            conditions.append(f"advertisement_price <= {self.price_max}")
        if self.location_region:
            conditions.append(f'advertisement_region = "{self.location_region}"')
        if self.location_city:
            conditions.append(f'advertisement_city = "{self.location_city}"')

        if conditions:
            query += " AND " + " AND ".join(conditions)

        if self.matches_text:
            query += f' AND (advertisement_name LIKE "%{self.matches_text}%" OR advertisement_description LIKE "%{self.matches_text}%")'

        if not conditions and not (self.sort_date or self.sort_price):
            query += " ORDER BY RANDOM()"

        elif self.sort_date:
            query += f" ORDER BY advertisement_date {self.sort_date}"

        elif self.sort_price:
            query += f" ORDER BY advertisement_price {self.sort_price}"

        print(query)

        cursor.execute(query, params)
        self.filtered_ads = cursor.fetchall()

        connect.close()

    def next_advertisement(self):
        if self.current_index < len(self.filtered_ads) - 1:
            self.current_index += 1

    def previous_advertisement(self):
        if self.current_index > 0:
            self.current_index -= 1

    def get_current_advertisement_info(self):
        if self.filtered_ads:
            return self.filtered_ads[self.current_index]
        else:
            return None


user_searches = {}


def get_user_search(user_id):
    if user_id not in user_searches:
        user_searches[user_id] = SearchAdsByBot()
    return user_searches[user_id]


def handle_start_search_advertisements(bot, message):
    search_ads = get_user_search(message.chat.id)
    search_ads.clear_index()
    search_ads.search_ads()
    current_ad_info = search_ads.get_current_advertisement_info()

    if not current_ad_info:
        bot.send_message(message.chat.id, "На жаль, за вашим запитом нічого не знайдено.")
        return

    else:
        ad_info = get_all_info_about_advertisement(current_ad_info[0])
        bot.send_message(message.chat.id, f"<b>⚠️ Оголошення №{search_ads.current_index + 1}/{len(search_ads.filtered_ads)}</b>",
                         parse_mode='HTML', reply_markup=ad_steps_keyboard)
        print_advertisement_info(bot, message, ad_info, search_ads)


def handle_previous_advertisement(bot, message):
    search_ads = get_user_search(message.chat.id)
    current_ad_info = search_ads.get_current_advertisement_info()

    if current_ad_info:
        if search_ads.current_index > 0:
            search_ads.previous_advertisement()
            current_index = search_ads.current_index
            total_ads = len(search_ads.filtered_ads)
            ad_info = get_all_info_about_advertisement(search_ads.filtered_ads[current_index][0])
            bot.send_message(message.chat.id, f"<b>⚠️ Оголошення №{current_index + 1}/{total_ads}</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
            print_advertisement_info(bot, message, ad_info, search_ads)
        else:
            bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до початку списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
    else:
        bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до початку списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)


def handle_next_advertisement(bot, message):
    search_ads = get_user_search(message.chat.id)
    current_ad_info = search_ads.get_current_advertisement_info()

    if current_ad_info:
        if search_ads.current_index < len(search_ads.filtered_ads) - 1:
            search_ads.next_advertisement()
            current_index = search_ads.current_index
            total_ads = len(search_ads.filtered_ads)
            ad_info = get_all_info_about_advertisement(search_ads.filtered_ads[current_index][0])
            bot.send_message(message.chat.id, f"<b>⚠️ Оголошення №{current_index + 1}/{total_ads}</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
            print_advertisement_info(bot, message, ad_info, search_ads)
        else:
            bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до кінця списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
    else:
        bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до кінця списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)


def print_advertisement_info(bot, message, ad_info, search_ads):
    price_uah = ad_info[7]
    formatted_price_uah = '{:,}'.format(price_uah).replace(',', ' ')

    converted_price_usd = convert_currency(price_uah, 'UAH', 'USD')
    formatted_price_usd = '{:,}'.format(converted_price_usd).replace(',', ' ')

    formatted_date = format_ukrainian_datetime(ad_info[8])

    adv_info = (
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
    add_to_favorites = types.InlineKeyboardButton("❤️ Додати у вибрані",
                                                  callback_data=f'add_to_favorites_btn{ad_info[0]}')
    complain = types.InlineKeyboardButton("⚠️ Поскаржитись на оголошення",
                                          callback_data=f'complain_btn{ad_info[0]}')
    ad_func.add(show_all_photos_button, show_contacts, add_to_favorites, complain)

    with open(photo_file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=adv_info, parse_mode="Markdown", reply_markup=ad_func)



# def handle_previous_advertisement(bot, message):
#     search_ads = get_user_search(message.chat.id)
#     current_ad_info = search_ads.get_current_advertisement_info()
#
#     if current_ad_info:
#         search_ads.previous_advertisement()
#         current_index = search_ads.current_index
#         total_ads = len(search_ads.filtered_ads)
#
#         if current_index == total_ads:
#             ad_info = get_all_info_about_advertisement(current_ad_info[0])
#             bot.send_message(message.chat.id, f"<b>⚠️ Оголошення №{current_index + 1}/{total_ads}</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
#             print_advertisement_info(bot, message, ad_info, search_ads)
#         else:
#             bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до кінця списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
#     else:
#         bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до кінця списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
#
#
# def handle_next_advertisement(bot, message):
#     search_ads = get_user_search(message.chat.id)
#     current_ad_info = search_ads.get_current_advertisement_info()  # Отримання інформації про поточне оголошення
#
#     if current_ad_info:
#         search_ads.next_advertisement()  # Переміщення до наступного оголошення
#         current_index = search_ads.current_index
#         total_ads = len(search_ads.filtered_ads)
#
#         if current_index == total_ads:
#             ad_info = get_all_info_about_advertisement(current_ad_info[0])
#             bot.send_message(message.chat.id, f"<b>⚠️ Оголошення №{current_index + 1}/{total_ads}</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
#             print_advertisement_info(bot, message, ad_info, search_ads)
#         else:
#             bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до кінця списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)
#     else:
#         bot.send_message(message.chat.id, "<b>❗️ Ви дійшли до кінця списку</b>", parse_mode='HTML', reply_markup=ad_steps_keyboard)