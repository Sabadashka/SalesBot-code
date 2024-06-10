from DataBase.BlockedUsers_database import delete_user_from_blocked, check_blocked_user_exists
from DataBase.Users_database import change_role_by_id
from Markups.markups import cancel_action
from Markups.menu_markups import admin_menu_database_keyboard_menu
from OtherTools import CancelAction


def unblock_user(bot, message, role):
    bot.send_message(message.chat.id, "❗️ Введіть *ID* користувача, якого Ви бажаєте *розблоквати*", parse_mode='Markdown', reply_markup=cancel_action)
    bot.register_next_step_handler(message, lambda msg: process_user_id(bot, msg, role))


def process_user_id(bot, message, role):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_block_user(message, bot, role)
        return

    user_id = message.text

    if check_blocked_user_exists(user_id):
        delete_user_from_blocked(user_id)
        bot.send_message(message.chat.id, f"❗️ Ви *розблокували* користувача\n*ID:* {user_id}", parse_mode='Markdown', reply_markup=admin_menu_database_keyboard_menu)
        change_role_by_id(user_id, 0)

    else:
        bot.send_message(message.chat.id, "❗️ *Користувача* з таким *ID* немає в *базі даних*, або він не є "
                                          "*заблокованим*", parse_mode='Markdown',
                         reply_markup=admin_menu_database_keyboard_menu)
        return