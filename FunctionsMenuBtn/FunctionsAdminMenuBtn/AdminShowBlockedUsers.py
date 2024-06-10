from DataBase.BlockedUsers_database import get_all_blocked_users_from_db
from Markups.menu_markups import keyboard_menu, admin_menu_keyboard_menu, admin_menu_database_keyboard_menu


def show_blocked_users(bot, message):
    users_data = get_all_blocked_users_from_db()

    if not users_data:
        bot.send_message(message.chat.id, "❗️ Немає заблокованих користувачів у базі даних.")
    else:
        users_message = "<b>Список заблокованих користувачів:</b>\n\n"
        for user_data in users_data:
            blocked_id = user_data[0]
            user_id = user_data[1]
            blocked_date = user_data[2]
            blocked_until = user_data[3]
            blocked_by_admin = user_data[5]
            user_info = (
                f"<b>Blocked_ID:</b> <code>{blocked_id}</code>\n"
                f"<b>ID:</b> <code>{user_id}</code>\n"
                f"<b>Дата блокування:</b> {blocked_date}\n"
                f"<b>Заблокований до:</b> {blocked_until}\n"
                f"<b>Заблокований адміністратором:</b> <code>{blocked_by_admin}</code>\n"
                "<b>----------------------</b>\n"
            )
            users_message += user_info

        bot.send_message(message.chat.id, users_message, parse_mode='HTML', reply_markup=admin_menu_database_keyboard_menu)
