from SearchAds.SearchAds import SearchAdsByBot
from SearchAds.SearchMessage import search_message

from telebot.types import Message
from telebot import types


def process_price_step(bot, message, user_search):
    price_selection_message = "<b>❗️ Введіть мінімальну ціну</b>"
    bot.send_message(message.chat.id, price_selection_message, parse_mode='HTML')

    bot.register_next_step_handler(message, lambda msg: process_min_price(bot, msg, user_search))


def process_min_price(bot, message, user_search):
    try:
        min_price = int(message.text)
        if min_price >= 100000000:
            bot.send_message(message.chat.id, "Мінімальна ціна не може бути більшою або рівною 100,000,000")
            bot.register_next_step_handler(message, lambda msg: process_min_price(bot, msg, user_search))
            return

        user_search.set_price_range(min_price, user_search.price_max)
        bot.send_message(message.chat.id, "<b>❗️ Введіть максимальну ціну</b>", parse_mode='HTML')
        bot.register_next_step_handler(message, lambda msg: process_max_price(bot, msg, user_search))
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть числове значення")
        bot.register_next_step_handler(message, lambda msg: process_min_price(bot, msg, user_search))


def process_max_price(bot, message, user_search):
    try:
        max_price = int(message.text)
        if max_price >= 100000000:
            bot.send_message(message.chat.id, "Максимальна ціна не може бути більшою або рівною 100,000,000")
            bot.register_next_step_handler(message, lambda msg: process_max_price(bot, msg, user_search))
            return
        if max_price <= user_search.price_min:
            bot.send_message(message.chat.id, "Максимальна ціна повинна бути більшою за мінімальну")
            bot.register_next_step_handler(message, lambda msg: process_max_price(bot, msg, user_search))
            return

        user_search.set_price_range(user_search.price_min, max_price)

        search_message(bot, message, user_search)
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть числове значення")
        bot.register_next_step_handler(message, lambda msg: process_max_price(bot, msg, user_search))
