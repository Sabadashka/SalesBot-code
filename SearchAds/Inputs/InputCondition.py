from telebot import types

from Messages.StartCreatingAdMessages import incorrect_condition_message
from OtherTools.CancelAction import cancel_advertisement_creation, cancel_filters_action
from SearchAds.SearchAds import SearchAdsByBot
from SearchAds.SearchMessage import search_message


def process_condition_step(bot, message, user_search):
    condition_selection_message = "<b>❗️ Оберіть стан товару</b>"

    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    markup_condition = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_condition.add(types.KeyboardButton('Нове'), types.KeyboardButton('Вживане'))
    markup_condition.add(types.KeyboardButton("❌ Скасувати дію"))
    bot.send_message(message.chat.id, condition_selection_message, parse_mode='HTML',
                     reply_markup=markup_condition)
    bot.register_next_step_handler(message, lambda message: process_condition_end(bot, message, user_search))


def process_condition_end(bot, message, user_search):
    if message.text == '❌ Скасувати дію':
        cancel_filters_action(message, bot)
        return

    user_search.condition = message.text

    if user_search.condition not in ['Нове', 'Вживане']:
        markup_condition = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_condition.add(types.KeyboardButton('Нове'), types.KeyboardButton('Вживане'))
        markup_condition.add(types.KeyboardButton("❌ Скасувати дію"))
        bot.send_message(message.chat.id, incorrect_condition_message, parse_mode='HTML', reply_markup=markup_condition)
        bot.register_next_step_handler(message, lambda message: process_condition_end(bot, message, user_search))
        return
    else:
        search_message(bot, message, user_search)
