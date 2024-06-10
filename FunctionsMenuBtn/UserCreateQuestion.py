from datetime import datetime

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from DataBase.Questions_database import create_new_question
from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu
from Notifications.ModeratorNotifications import notification_new_location_ad, notification_new_question
from OtherTools.CancelAction import cancel_question_creation
from OtherTools.MonthConverter import format_ukrainian_datetime_with_year_for_notifications


def start_creating_question(bot, call, acc_id):
    if call.message.text == '❌ Скасувати дію':
        cancel_question_creation(call, bot)
        return

    bot.send_message(call.message.chat.id, "<b>❗️ Введіть Ваше запитання</b>", parse_mode='HTML', reply_markup=cancel_action)
    bot.register_next_step_handler(call.message, process_question_text, bot, acc_id)


def process_question_text(message, bot, acc_id):
    question_text = message.text

    if message.text == '❌ Скасувати дію':
        cancel_question_creation(message, bot)
        return

    if len(question_text) > 350:
        bot.send_message(message.chat.id,
                         "<b>❗️ Запитання не може бути більше 350 символів</b>\n\n⚠️ <i>Спробуйте ще раз</i>", parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, process_question_text, bot, acc_id)

    else:

        question_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date = format_ukrainian_datetime_with_year_for_notifications(question_date)
        question_message = (
            f"<b>❗️ Ваше запитання надіслано</b>\n\n"
            f"<b>❓ Запитання:</b> {question_text}\n\n"
            f"<b>{'-' * 40}</b>\n"
            f"<b>🗓 Дата:</b> {date}"
        )

        bot.send_message(message.chat.id, question_message, parse_mode='HTML', reply_markup=keyboard_menu)
        create_new_question(acc_id, question_text)
        notification_new_question(bot, acc_id)
