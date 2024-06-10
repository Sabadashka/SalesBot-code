from Markups.menu_markups import keyboard_menu


def main_menu(bot, message):
    bot.send_message(message.chat.id, f"❗️ Ви вийшли в '*Головне меню*'", parse_mode='Markdown',
                     reply_markup=keyboard_menu)
