from telebot import types

from OtherTools.CancelAction import cancel_filters_action
from SearchAds.SearchMessage import search_message


def process_sort_by(bot, message, user_search):
    choice_sort_message = "<b>❗️ Оберіть за тип сортування:</b>"
    sort_markup_date = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sort_markup_date.add(types.KeyboardButton('За датою'), types.KeyboardButton('За ціною'))
    sort_markup_date.add(types.KeyboardButton("❌ Скасувати дію"))
    bot.register_next_step_handler(message, lambda message: process_choice_sort_by(bot, message, user_search))
    bot.send_message(message.chat.id, choice_sort_message, parse_mode='HTML', reply_markup=sort_markup_date)


def process_choice_sort_by(bot, message, user_search):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    choice = message.text

    if choice not in ['За датою', 'За ціною']:
        choice_sort_message = "<b>❗️ Оберіть за тип сортування:</b>"
        sort_markup_date = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sort_markup_date.add(types.KeyboardButton('За датою'), types.KeyboardButton('За ціною'))
        sort_markup_date.add(types.KeyboardButton("❌ Скасувати дію"))
        bot.send_message(message.chat.id, choice_sort_message, parse_mode='HTML', reply_markup=sort_markup_date)
        bot.register_next_step_handler(message, lambda message: process_choice_sort_by(bot, message, user_search))

    else:
        if message.text == 'За датою':
            process_sort_by_date_step(bot, message, user_search)
            return

        elif message.text == 'За ціною':
            process_sort_by_price_step(bot, message, user_search)
            return


def process_sort_by_date_step(bot, message, user_search):
    sort_message = "<b>❗️ Оберіть за якою датою сортувати пошук</b>"

    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    sort_markup_date = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sort_markup_date.add(types.KeyboardButton('Найновіші оголошення'), types.KeyboardButton('Найстаріші оголошення'))
    sort_markup_date.add(types.KeyboardButton("❌ Скасувати дію"))
    bot.send_message(message.chat.id, sort_message, parse_mode='HTML',
                     reply_markup=sort_markup_date)
    bot.register_next_step_handler(message, lambda message: process_sort_by_date_end(bot, message, user_search))


def process_sort_by_date_end(bot, message, user_search):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    sort_type_message = message.text

    if sort_type_message not in ['Найновіші оголошення', 'Найстаріші оголошення']:
        sort_markup_date = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sort_markup_date.add(types.KeyboardButton('Найновіші оголошення'),
                             types.KeyboardButton('Найстаріші оголошення'))
        sort_markup_date.add(types.KeyboardButton("❌ Скасувати дію"))

        invalid_sort_type = "<b>❌ Некоректний тип сортування. Потрібно обрати зі списку доступних</b>"

        bot.send_message(message.chat.id, invalid_sort_type, parse_mode='HTML', reply_markup=sort_markup_date)
        bot.register_next_step_handler(message, lambda message: process_sort_by_date_end(bot, message, user_search))
        return
    else:
        if sort_type_message == 'Найстаріші оголошення':
            type_name = 'ASC'
            user_search.sort_date = type_name
            user_search.clear_sort_price()
            search_message(bot, message, user_search)
            return

        elif sort_type_message == 'Найновіші оголошення':
            types_name = 'DESC'
            user_search.sort_date = types_name
            user_search.clear_sort_price()
            search_message(bot, message, user_search)
            return


def process_sort_by_price_step(bot, message, user_search):
    sort_message = "<b>❗️ Оберіть за якою ціною сортувати пошук</b>"

    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    sort_markup_price = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sort_markup_price.add(types.KeyboardButton('Найменша ціна'), types.KeyboardButton('Найбільша ціна'))
    sort_markup_price.add(types.KeyboardButton("❌ Скасувати дію"))
    bot.send_message(message.chat.id, sort_message, parse_mode='HTML',
                     reply_markup=sort_markup_price)
    bot.register_next_step_handler(message, lambda message: process_sort_by_price_end(bot, message, user_search))


def process_sort_by_price_end(bot, message, user_search):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    sort_type_message = message.text

    if sort_type_message not in ['Найменша ціна', 'Найбільша ціна']:
        sort_markup_price = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sort_markup_price.add(types.KeyboardButton('Найменша ціна'), types.KeyboardButton('Найбільша ціна'))
        sort_markup_price.add(types.KeyboardButton("❌ Скасувати дію"))

        invalid_sort_type = "<b>❌ Некоректний тип сортування. Потрібно обрати зі списку доступних</b>"

        bot.send_message(message.chat.id, invalid_sort_type, parse_mode='HTML', reply_markup=sort_markup_price)
        bot.register_next_step_handler(message, lambda message: process_sort_by_price_end(bot, message, user_search))
        return
    else:
        if sort_type_message == 'Найменша ціна':
            type_name = 'ASC'
            user_search.sort_price = type_name
            user_search.clear_sort_date()
            search_message(bot, message, user_search)
            return

        elif sort_type_message == 'Найбільша ціна':
            types_name = 'DESC'
            user_search.sort_price = types_name
            user_search.clear_sort_date()
            search_message(bot, message, user_search)
            return
