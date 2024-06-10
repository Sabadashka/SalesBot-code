from datetime import datetime

import telebot

from DataBase.Users_database import get_all_users_id
from telebot import TeleBot
from telebot.types import Message

from Markups.markups import cancel_action
from Markups.menu_markups import admin_menu_database_keyboard_menu, admin_menu_keyboard_menu
from Notifications.UserNotifications import make_notification_by_administrator
from OtherTools import CancelAction
from OtherTools.MonthConverter import format_ukrainian_datetime_with_year_for_notifications


def start_creating_notification(bot: TeleBot, message: Message, role: int):
    bot.send_message(message.chat.id, "<b>❗️ Введіть заголовок сповіщення</b>", parse_mode='HTML', reply_markup=cancel_action)
    bot.register_next_step_handler(message, process_notification_title, bot, role)


def process_notification_title(message: Message, bot: TeleBot, role: int):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_make_notification(message, bot, role)
        return

    notification_title = message.text

    if len(notification_title) > 45:
        bot.send_message(message.chat.id,
                         "<b>❗️ Заголовок не може бути більше 45 символів</b>\n\n⚠️ <i>Спробуйте ще раз</i>", parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, process_notification_title, bot)

    else:
        bot.send_message(message.chat.id, "<b>❗️ Введіть текст сповіщення</b>", parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, process_notification_text, bot, role, notification_title)


def process_notification_text(message: Message, bot: TeleBot, role: int, notification_title: str):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_make_notification(message, bot, role)
        return

    notification_text = message.text

    if len(notification_text) > 650:
        bot.send_message(message.chat.id,
                         "<b>❗️ Текст не може бути більше 650 символів</b>\n\n⚠️ <i>Спробуйте ще раз</i>", parse_mode='HTML', reply_markup=cancel_action)
        bot.register_next_step_handler(message, process_notification_text, bot, role, notification_text)

    else:
        users_id = get_all_users_id()

        notification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date = format_ukrainian_datetime_with_year_for_notifications(notification_date)

        notification_message = (
            f"<b>❗️ Ваше сповіщення:</b>\n"
            f"<b>🔔️ Сповіщення:</b> {notification_title}\n\n"
            f"<b>📢 Текст:</b> <i>{notification_text}</i>\n"
            f"<b>{'-' * 40}</b>\n"
            f"<b>🗓 Дата:</b> {date}"
        )

        bot.send_message(message.chat.id, notification_message, parse_mode='HTML', reply_markup=admin_menu_keyboard_menu)

        for telegram_id in users_id:
            try:
                make_notification_by_administrator(bot, telegram_id, notification_title, notification_text)
            except telebot.apihelper.ApiTelegramException as e:
                if e.result_json['description'] == 'Forbidden: bot was blocked by the user':
                    print(f"Користувач {telegram_id} заблокував бота. Повідомлення не надіслано.")
                else:
                    print(f"Помилка при надсиланні повідомлення користувачу {telegram_id}: {e}")