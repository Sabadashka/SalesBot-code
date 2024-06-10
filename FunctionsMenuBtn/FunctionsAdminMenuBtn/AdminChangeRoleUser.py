from DataBase.Users_database import check_user_exists, change_role_by_id
from Markups.markups import cancel_action
from Markups.menu_markups import admin_menu_database_keyboard_menu
from OtherTools import CancelAction


def change_role(bot, message, role):
    bot.send_message(message.chat.id, "❗️ *Введіть ID користувача*, якому бажаєте змінити *роль*", parse_mode='Markdown', reply_markup=cancel_action)
    bot.register_next_step_handler(message, lambda msg: process_change_role(bot, msg, role))


def process_change_role(bot, message, role):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_change_user_role(message, bot, role)
        return

    user_id = message.text.strip()

    if check_user_exists(user_id):
        bot.send_message(message.chat.id, "❗️ *Введіть номер ролі, яку бажаєте видати:*\n*0.* 👥 Користувач\n*1.* 🛡️ Модератор\n*2.* 👑️ Адміністратор", parse_mode='Markdown', reply_markup=cancel_action)
        bot.register_next_step_handler(message, lambda msg: process_role_input(bot, msg, user_id, role))
    else:
        bot.send_message(message.chat.id, "❗️ *Користувача* з таким *ID* немає в *базі даних*", parse_mode='Markdown', reply_markup=admin_menu_database_keyboard_menu)
        return


def process_role_input(bot, message, user_id, role):
    if message.text == '❌ Скасувати дію':
        CancelAction.cancel_change_user_role(message, bot, role)
        return

    user_role = message.text

    if user_role == "0":
        bot.send_message(message.chat.id, f"❗️ <b>Ви змінили користувачу</b>\n<b>ID:</b> <code>{user_id}</code>\n<b>Нова роль:</b> 👥 Користувач",
                         parse_mode='HTML', reply_markup=admin_menu_database_keyboard_menu)
        change_role_by_id(user_id, 0)

    elif user_role == "1":
        bot.send_message(message.chat.id, f"❗️ <b>Ви змінили користувачу</b>\n<b>ID:</b> <code>{user_id}</code>\n<b>Нова роль:</b> 🛡️ Модератор",
                         parse_mode='HTML', reply_markup=admin_menu_database_keyboard_menu)
        change_role_by_id(user_id, 1)

    elif user_role == "2":
        bot.send_message(message.chat.id, f"❗️ <b>Ви змінили користувачу</b>\n<b>ID:</b> <code>{user_id}</code>\n<b>Нова роль:</b> 👑️ Адміністратор",
                         parse_mode='HTML', reply_markup=admin_menu_database_keyboard_menu)
        change_role_by_id(user_id, 2)

    else:
        bot.send_message(message.chat.id, "❗️ <b>Такої ролі не існує</b>", parse_mode='Markdown', reply_markup=admin_menu_database_keyboard_menu)
        return
