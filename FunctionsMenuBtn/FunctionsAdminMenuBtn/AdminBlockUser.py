from pydantic.v1.datetime_parse import parse_date

from DataBase.BlockedUsers_database import create_new_blocked_user
from DataBase.Users_database import change_role_by_id, check_user_exists
from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu, admin_menu_keyboard_menu, admin_menu_database_keyboard_menu
from datetime import datetime, timedelta

from OtherTools import CancelAction


def block_user(bot, admin_id, message, role):
    bot.send_message(admin_id, "❗️ Введіть *ID користувача*, якого Ви бажаєте заблокувати", parse_mode='Markdown', reply_markup=cancel_action)
    bot.register_next_step_handler(message, lambda msg: process_user_id(bot, admin_id, msg, role))


def process_user_id(bot, admin_id, message, role):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_block_user(message, bot, role)
        return

    user_id = message.text

    if check_user_exists(user_id):
        bot.send_message(message.chat.id, "❗️ Введіть на скільки *днів* заблокувати користувача", parse_mode='Markdown', reply_markup=cancel_action)
        bot.register_next_step_handler(message, lambda msg: process_blocked_until(bot, admin_id, user_id, msg, role))
    else:
        bot.send_message(message.chat.id, "❗️ *Користувача* з таким *ID* немає в *базі даних*", parse_mode='Markdown', reply_markup=admin_menu_database_keyboard_menu)
        return


def process_blocked_until(bot, admin_id, user_id, message, role):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_block_user(message, bot, role)
        return

    try:
        blocked_until_input = message.text

        if blocked_until_input.isdigit():
            days = int(blocked_until_input)
            blocked_until = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            blocked_until = parse_date(blocked_until_input).strftime("%Y-%m-%d %H:%M:%S")

        bot.send_message(message.chat.id, "❗️ Введіть *причину блокування*:", parse_mode='Markdown', reply_markup=cancel_action)
        bot.register_next_step_handler(message,
                                       lambda msg: process_blocked_reason(bot, admin_id, user_id, blocked_until, msg, role))
    except Exception as e:
        bot.send_message(message.chat.id, f"❗️ Помилка при обробці дати розблокування: *{str(e)}*", parse_mode='Markdown', reply_markup=admin_menu_database_keyboard_menu)


def process_blocked_reason(bot, admin_id, user_id, blocked_until, message, role):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_block_user(message, bot, role)
        return

    blocked_reason = message.text
    create_new_blocked_user(user_id, blocked_until, blocked_reason, admin_id)
    bot.send_message(message.chat.id, f"❗️ *Ви заблокували користувача ID:* {user_id}.\n❌ *Причина блокування:* {blocked_reason}", parse_mode='Markdown', reply_markup=admin_menu_database_keyboard_menu)
    change_role_by_id(user_id, -1)

