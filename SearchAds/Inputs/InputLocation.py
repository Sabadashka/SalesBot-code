from telebot import types

from Markups.creating_ad_category_region_markups import regions, cities
from OtherTools.CancelAction import cancel_filters_action
from SearchAds.SearchMessage import search_message


def process_location_region_step(bot, message, user_search):
    category_selection_message = "<b>❗️ Оберіть область для пошуку</b>"

    markup_region = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for region in regions:
        markup_region.add(types.KeyboardButton(region))
    markup_region.add(types.KeyboardButton("❌ Скасувати дію"))

    bot.send_message(message.chat.id, category_selection_message, parse_mode='HTML', reply_markup=markup_region)
    bot.register_next_step_handler(message, lambda message: process_location_region_end(bot, message, user_search))


def process_location_region_end(bot, message, user_search):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    region = message.text
    cities_list = cities.get(region, [])

    if cities_list:
        user_search.location_region = region

        markup_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for city in cities_list:
            markup_cities.add(types.KeyboardButton(city))
        markup_cities.add(types.KeyboardButton("❌ Скасувати дію"))

        city_selection_message = f"❗️ <b>Оберіть Ваше місто в {region}</b>"
        bot.send_message(message.chat.id, city_selection_message, parse_mode='HTML', reply_markup=markup_cities)

        bot.register_next_step_handler(message, lambda message: process_location_city_end(bot, message, user_search, region))
    else:
        error_region_selection_message = "🌟  <b>Потрібно обрати область зі списку</b>\n\n"

        markup_region = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for region in regions:
            markup_region.add(types.KeyboardButton(region))
        markup_region.add(types.KeyboardButton("❌ Скасувати дію"))
        bot.send_message(message.chat.id, error_region_selection_message, parse_mode='HTML', reply_markup=markup_region)
        bot.register_next_step_handler(message, lambda message: process_location_region_end(bot, message, user_search))


def process_location_city_end(bot, message, user_search, region):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    city = message.text

    cities_list = cities.get(region, [])
    if city not in cities_list:
        markup_cities = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for city in cities_list:
            markup_cities.add(types.KeyboardButton(city))
        markup_cities.add(types.KeyboardButton("❌ Скасувати дію"))

        error_city_selection_message = "🌟  <b>Потрібно обрати місто зі списку</b>"

        bot.send_message(message.chat.id, error_city_selection_message, parse_mode='HTML', reply_markup=markup_cities)
        bot.register_next_step_handler(message, lambda message: process_location_city_end(bot, message, user_search, region))
        return

    else:
        user_search.location_city = city
        search_message(bot, message, user_search)

