from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from DataBase.Advertisement_database import create_advertisement
from telebot import TeleBot, types
from datetime import datetime

from Markups.markups import cancel_action, markup_reg, start_bot_keyboard
from Markups.menu_markups import keyboard_menu
from OtherTools.CheckRole import check_role_for_database_actions, check_role_for_show_admins, \
    check_role_to_return_to_apanel_menu


def cancel_registration_button(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, "<b>❗️ Ви скасували реєстрацію</b>", parse_mode='HTML', reply_markup=start_bot_keyboard)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_advertisement_creation(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, "<b>❗ Створення оголошення скасовано</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_question_creation(call, bot):
    bot.send_message(call.chat.id, "<b>❗ Створення оголошення скасовано</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=call.chat.id)


def cancel_filters_action(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували налаштування фільтру</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_block_user(message, bot, role):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували блокування користувача</b>", parse_mode='HTML')

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    check_role_for_database_actions(role, bot, message)


def cancel_unblock_user(message, bot, role):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували розблокування користувача</b>", parse_mode='HTML')

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    check_role_for_database_actions(role, bot, message)


def cancel_make_notification(message, bot, role):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували створення сповіщення</b>", parse_mode='HTML')

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    check_role_to_return_to_apanel_menu(role, bot, message)


def cancel_change_user_role(message, bot, role):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували зміну ролі користувачу</b>", parse_mode='HTML')

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    check_role_for_database_actions(role, bot, message)


def cancel_change_new_name_ad_action(bot, message):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували зміну імені оголошення</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_change_description_ad_action(bot, message):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували зміну опису оголошення</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_change_photos_ad_action(message: Message, bot: TeleBot):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували оновлення фото оголошення</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_change_price_ad_action(bot, message):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували зміну ціни оголошення</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)


def cancel_change_location_ad_action(bot, message):
    bot.send_message(message.chat.id, "<b>❗ Ви скасували зміну місцезнаходження оголошення</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)