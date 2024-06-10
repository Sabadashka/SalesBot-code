from DataBase.Users_database import get_all_users_from_db
from Markups.menu_markups import admin_keyboard_menu, admin_menu_keyboard_menu, keyboard_menu, \
    admin_menu_database_keyboard_menu


def show_users_by_role(bot, message, role):
    user_roles = {
        0: "Користувач",
        1: "Модератор",
        2: "Адміністратор"
    }

    users_data = get_all_users_from_db()

    if not users_data:
        bot.send_message(message.chat.id, "❗️ Немає користувачів у базі даних.")
    else:
        users_by_role = {-1: [], 0: [], 1: [], 2: []}

        for user_data in users_data:
            user_id = user_data[0]
            user_name = user_data[1]
            user_mail = user_data[2]
            user_role = user_data[5]

            users_by_role[user_role].append((user_id, user_name, user_mail, user_role))

        users_message = ""

        if users_by_role[role]:
            users_message += f"<b>Список {user_roles[role]}ів:</b>\n\n"
            for user_data in users_by_role[role]:
                user_id = user_data[0]
                user_name = user_data[1]
                user_mail = user_data[2]
                user_info = (
                    f"<b>ID:</b> <code>{user_id}</code>\n"
                    f"<b>Ім'я:</b> {user_name}\n"
                    f"<b>Пошта:</b> {user_mail}\n"
                    "<b>----------------------</b>\n"
                )
                users_message += user_info

        users_count_message = f"\n<b>Кількість {user_roles[role]}ів:</b> {len(users_by_role[role])}\n"

        bot.send_message(message.chat.id, users_message + users_count_message, parse_mode='HTML',
                         reply_markup=admin_menu_database_keyboard_menu)