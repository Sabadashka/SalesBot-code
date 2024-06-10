from DataBase.Users_database import set_new_name
from FunctionsMenuBtn.UserShowProfile import show_user_profile_back
from Markups.menu_markups import keyboard_menu
from Markups.user_profile_markups import cancel_name_edit_markup, profile_settings_markups
from Validation.NameValidation import validate_name


def new_name(bot, message):
    bot.send_message(message.chat.id, "<b>❗️ Введіть нове ім'я</b>", parse_mode='HTML', reply_markup=cancel_name_edit_markup)

    bot.register_next_step_handler(message, lambda msg: process_new_name_input(bot, msg))


def process_new_name_input(bot, message):
    new_name = message.text

    if message.text == '❌ Скасувати зміну імені':
        cancel_new_name_creation(message, bot)
        return

    acc_id = message.from_user.id

    if validate_name(new_name):
        set_new_name(acc_id, new_name)
        bot.send_message(message.chat.id, f"Ім'я успішно змінено на *{new_name}*", parse_mode='Markdown',
                         reply_markup=keyboard_menu)
        new = show_user_profile_back(message)
        bot.send_message(message.chat.id, new, parse_mode='HTML',
                         reply_markup=profile_settings_markups)
    else:
        bot.send_message(message.chat.id,
                         'Неправильний формат імені. Введіть ім\'я у форматі "Ім\'я Прізвище". Введіть ще раз...', reply_markup=cancel_name_edit_markup)
        bot.register_next_step_handler(message, lambda msg: process_new_name_input(bot, msg))


def cancel_new_name_creation(message, bot):
    bot.send_message(message.chat.id, "❗️ Зміну імені скасовано", reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)