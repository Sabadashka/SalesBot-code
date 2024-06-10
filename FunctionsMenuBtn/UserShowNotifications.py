from DataBase.Notifications_database import get_notifications_by_user_id, get_notification_by_id, \
    change_notification_status
from OtherTools.MonthConverter import format_ukrainian_datetime_with_year_for_notifications
from telebot import types


def display_notifications(bot, message_or_call):
    if isinstance(message_or_call, types.Message):
        chat_id = message_or_call.chat.id
    elif isinstance(message_or_call, types.CallbackQuery):
        chat_id = message_or_call.message.chat.id
    else:
        return

    notifications = get_notifications_by_user_id(chat_id)

    if not notifications:
        text = "😥 <b>У Вас немає сповіщень</b>"
        bot.send_message(chat_id, text, parse_mode='HTML')
    else:
        text = "<b>🔔️ Список Ваших сповіщень:</b>\n\n"
        notification_settings = types.InlineKeyboardMarkup(row_width=1)

        sorted_notifications = sorted(notifications, key=lambda x: x[5], reverse=True)

        latest_notifications = sorted_notifications[:5]

        for notification in latest_notifications:
            notification_id = notification[0]
            notification_title = notification[2]
            notification_status = notification[4]

            notification_show = types.InlineKeyboardButton(f"[{notification_status}] | {notification_title}", callback_data=f'show_notification{notification[0]}')
            notification_settings.add(notification_show)

        bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=notification_settings)


def show_notification(bot, call, notification_id):
    notification = get_notification_by_id(notification_id)

    if notification:
        notification_id, telegram_id, notification_title, notification_text, notification_status, notification_date = notification

        date = format_ukrainian_datetime_with_year_for_notifications(notification_date)
        notification_message = (
            f"<b>🔔️ Сповіщення:</b> {notification_title}\n\n"
            f"<b>📢 Текст:</b> <i>{notification_text}</i>\n"
            f"<b>{'-' * 40}</b>\n"
            f"<b>🗓 Дата:</b> {date}"
        )

        notification_buttons = types.InlineKeyboardMarkup(row_width=1)
        go_back_notifications_button = types.InlineKeyboardButton(f"◀️ Повернутися назад", callback_data=f'go_back_notifications')
        notification_buttons.add(go_back_notifications_button)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=notification_message, parse_mode='HTML', reply_markup=notification_buttons)
        change_notification_status(notification_id, 'Переглянуто')

    else:
        bot.send_message(call.message.chat.id, "<b>❗️ Щось пішло не так... Або цього сповіщення не існує більше...</b>")

