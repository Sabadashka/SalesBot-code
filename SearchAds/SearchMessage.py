import math

from telebot import types

from Markups.menu_markups import keyboard_search_menu, keyboard_menu
from SearchAds.FiltersButtons import get_matches_text_button, get_category_and_subcategory_button, \
    get_price_min_max_callback, get_location_button, get_sort_by_button, get_condition_button
from SearchAds.SearchAds import SearchAdsByBot, get_user_search

search_ads = SearchAdsByBot()


def search_message(bot, message, user_search):
    search_message_text = "🌟<b> Параметри пошуку:</b>\n\n"

    if user_search.matches_text:
        search_message_text += f"📌 Текст збігів: {user_search.matches_text}\n"

    if user_search.condition:
        search_message_text += f"📌 Стан: {user_search.condition}\n"

    if user_search.category and user_search.subcategory:
        search_message_text += f"📌 Категорія: {user_search.category} -> Підкатегорія: {user_search.subcategory}\n"

    if user_search.price_min is not None and user_search.price_max is not None:
        if not (user_search.price_min == 0 and math.isinf(user_search.price_max)):
            search_message_text += f"📌 Ціна від: {user_search.price_min} до {user_search.price_max}\n"

    if user_search.location_region and user_search.location_city:
        search_message_text += f"📌 Місцезнаходження: {user_search.location_region}, {user_search.location_city}\n"

    if user_search.sort_date:
        if user_search.sort_date == 'DESC':
            sort_name = 'Найновіші оголошення'
            search_message_text += f"📌 Сортування за датою: {sort_name}\n"

        elif user_search.sort_date == 'ASC':
            sort_name = 'Найстаріші оголошення'
            search_message_text += f"📌 Сортування за датою: {sort_name}\n"

    elif user_search.sort_price:
        if user_search.sort_price == 'DESC':
            sort_name = 'Найбільша ціна'
            search_message_text += f"📌 Сортування за ціною: {sort_name}\n"

        elif user_search.sort_price == 'ASC':
            sort_name = 'Найменша ціна'
            search_message_text += f"📌 Сортування за ціною: {sort_name}\n"

    if not (user_search.matches_text or user_search.condition or (user_search.category and user_search.subcategory) or (
            (user_search.price_min is not None and user_search.price_max is not None and
             not (user_search.price_min == 0 and user_search.price_max == float('inf')))) or
            (
                    user_search.location_region and user_search.location_city) or user_search.sort_date or user_search.sort_price):
        search_message_text += "<b><i>❗️ У Вас ще не вказано фільтрів пошуку:</i></b>\n<i> - Натисніть кнопку <b>'⚙️ Налаштування фільтрів пошуку'</b>, щоб їх налаштувати</i>\n"

    search_ads_filter_settings = types.InlineKeyboardMarkup(row_width=1)
    filters_settings_btn = types.InlineKeyboardButton("⚙️ Налаштування пошуку", callback_data=f'filters_settings_btn')
    search_ads_filter_settings.add(filters_settings_btn)

    bot.send_message(message.chat.id, "<b>❗️ Інструкція</b>\n<i>    - Якщо Ви налаштували фільтри пошуку/сортування пошуку, то натисність клавіатурну кнопку <b>'🚀 Виконати пошук'</b></i>", parse_mode='HTML',
                     reply_markup=keyboard_search_menu)
    bot.send_message(message.chat.id, search_message_text, parse_mode='HTML', reply_markup=search_ads_filter_settings)


def search_filters_message(bot, message, user_search):
    search_filters_message_text = "<b>❗️ Оберіть, який фільтер бажаєте змінити:</b>"

    filters_search_func_buttons = types.InlineKeyboardMarkup(row_width=1)

    matches_text_btn_text, callback = get_matches_text_button(user_search)
    matches_text_btn = types.InlineKeyboardButton(matches_text_btn_text, callback_data=callback)

    condition_btn_text, callback = get_condition_button(user_search)
    condition_btn = types.InlineKeyboardButton(condition_btn_text, callback_data=callback)

    category_and_subcategory_btn_text, callback = get_category_and_subcategory_button(user_search)
    category_and_subcategory_btn = types.InlineKeyboardButton(category_and_subcategory_btn_text, callback_data=callback)

    price_min_max_btn_text, callback = get_price_min_max_callback(user_search)
    price_min_max_btn = types.InlineKeyboardButton(price_min_max_btn_text, callback_data=callback)

    location_btn_text, callback = get_location_button(user_search)
    location_btn = types.InlineKeyboardButton(location_btn_text, callback_data=callback)

    sort_by_btn_text, callback = get_sort_by_button(user_search)
    sort_by_btn = types.InlineKeyboardButton(sort_by_btn_text, callback_data=callback)

    cancel_all_filters_btn = types.InlineKeyboardButton("❌ Скасувати введені параметри пошуку ❌", callback_data='cancel_all_filters_btn')
    back_to_message_filters_btn = types.InlineKeyboardButton("◀️ Назад", callback_data='back_to_message_filters_btn')

    filters_search_func_buttons.add(matches_text_btn, condition_btn, category_and_subcategory_btn, price_min_max_btn, location_btn, sort_by_btn, cancel_all_filters_btn, back_to_message_filters_btn)

    bot.send_message(message.chat.id, search_filters_message_text, parse_mode='HTML', reply_markup=filters_search_func_buttons)
