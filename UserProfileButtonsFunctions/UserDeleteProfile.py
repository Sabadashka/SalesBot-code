from telebot import TeleBot, types
from DataBase.Users_database import delete_user_data, check_password, get_user_mail
from Mail.MailVerification import send_verification_code
from Markups.markups import start_bot_keyboard
from Markups.menu_markups import keyboard_menu
from Messages.StartBotMessages import confirmation_code_message


def delete_account(bot, chat_id):
    markup_yes_no = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton("Так, впевнений.", callback_data='yes_btn')
    no_btn = types.InlineKeyboardButton("Ні, не видаляти аккаунт", callback_data='no_btn')
    markup_yes_no.add(yes_btn, no_btn)

    bot.send_message(chat_id, '<b>❗️ Підтвердіть дію...</b>', parse_mode="HTML", reply_markup=markup_yes_no)


def yes_delete_profile(bot, message, acc_id, message_id):
    user_mail = get_user_mail(acc_id)

    if user_mail is not None:
        bot.edit_message_text(chat_id=acc_id, message_id=message_id, text=f'Ваш емейл: {user_mail}')
        #bot.edit_message_text(chat_id=acc_id, message_id=message_id)
    else:
        bot.send_message(message.chat.id, '<b>❗️ Користувач не зареєстрований або електронна пошта відсутня</b>', parse_mode='HTML')

    verification_code = send_verification_code(user_mail)

    bot.send_message(message.chat.id, confirmation_code_message, parse_mode='HTML')

    bot.register_next_step_handler(message, lambda msg: handle_code_input(bot, msg, verification_code, acc_id))


def no_delete_profile(bot, message, chat_id, message_id):
    text = "<b>😊 Обліковий запис не видалено</b>"

    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=keyboard_menu)


def handle_code_input(bot, message, verification_code, acc_id):
    user_entered_code = message.text.strip()

    if user_entered_code.isdigit() and int(user_entered_code) == verification_code:

        bot.send_message(message.chat.id, '<b>❗️ Пошту підтверджено!</b>', parse_mode='HTML')
        delete_user_data(acc_id)
        bot.send_message(acc_id, '<b>😓 Обліковий запис успішно видалено</b>', parse_mode='HTML', reply_markup=start_bot_keyboard)
    else:
        bot.send_message(message.chat.id, '<b>❗️ Неправильний код підтвердження</b> \n\n<i>😊 Обліковий запис не видалено</i>', parse_mode="HTML", reply_markup=keyboard_menu)

