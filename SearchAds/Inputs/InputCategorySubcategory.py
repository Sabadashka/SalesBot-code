from telebot import types
from Markups.creating_ad_category_region_markups import categories, subcategories
from OtherTools.CancelAction import cancel_filters_action
from SearchAds.SearchMessage import search_message


def process_category_step(bot, message, user_search):
    category_selection_message = "<b>❗️ Оберіть категорію для пошуку</b>"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for category in categories:
        markup.add(types.KeyboardButton(category))
    markup.add(types.KeyboardButton("❌ Скасувати дію"))

    bot.send_message(message.chat.id, category_selection_message, parse_mode='HTML', reply_markup=markup)
    bot.register_next_step_handler(message, lambda message: process_category_end(bot, message, user_search))


def process_category_end(bot, message, user_search):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    category = message.text
    subcategory_list = subcategories.get(category, [])

    if category in categories:
        if subcategory_list:
            user_search.category = category

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for subcategory in subcategory_list:
                markup.add(types.KeyboardButton(subcategory))
            markup.add(types.KeyboardButton("❌ Скасувати дію"))

            subcategory_selection_message = f"2️⃣ <b>Оберіть підкатегорію для '{user_search.category}'</b>"
            bot.send_message(message.chat.id, subcategory_selection_message, parse_mode='HTML',
                             reply_markup=markup)

            bot.register_next_step_handler(message,
                                           lambda message: process_subcategory_end(bot, message, user_search, category))
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for category in categories:
            markup.add(types.KeyboardButton(category))
        markup.add(types.KeyboardButton("❌ Скасувати дію"))

        category_error_selection_message = "🌟 <b>Потрібно обрати категорію зі списку</b>\n\n"

        bot.send_message(message.chat.id, category_error_selection_message, parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, lambda message: process_category_end(bot, message, user_search))


def process_subcategory_end(bot, message, user_search, category):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    subcategory = message.text
    subcategory_list = subcategories.get(category, [])

    if subcategory not in subcategory_list:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, )
        for subcategory in subcategory_list:
            markup.add(types.KeyboardButton(subcategory))
        markup.add(types.KeyboardButton("❌ Скасувати дію"))
        subcategory_error_selection_message = "<b>🌟 Потрібно обрати підкатегорію зі списку</b>\n\n"

        bot.send_message(message.chat.id, subcategory_error_selection_message,
                         parse_mode='HTML', reply_markup=markup)
        bot.register_next_step_handler(message, process_subcategory_end, bot, user_search, category)

    else:
        user_search.subcategory = subcategory
        search_message(bot, message, user_search)
