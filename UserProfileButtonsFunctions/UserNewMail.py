from DataBase.Users_database import set_new_mail, get_user_data_by_telegram_id
from FunctionsMenuBtn.UserShowProfile import show_user_profile_back
from Mail.MailVerification import send_verification_code
from Markups.menu_markups import keyboard_menu
from Markups.user_profile_markups import cancel_mail_edit_markup, profile_settings_markups
from Messages.StartBotMessages import confirmation_code_message, invalid_email_message
from OtherTools.CancelAction import cancel_registration_button
from Validation.MailValidation import validate_email


def process_change_mail(bot, message):
    acc_id = message.chat.id
    user_data = get_user_data_by_telegram_id(acc_id)

    if user_data is not None:
        mail = user_data[2]

        bot.send_message(message.chat.id, confirmation_code_message, parse_mode="HTML", reply_markup=cancel_mail_edit_markup)

        verification_code = send_verification_code(mail)
        bot.register_next_step_handler(message, lambda msg: check_verification_code(msg, bot, acc_id, verification_code))
    else:
        bot.send_message(message.chat.id, "Користувача не знайдено")


def check_verification_code(message, bot, acc_id, sent_verification_code):
    if message.text == "❌ Скасувати зміну скиньки":
        cancel_new_mail_creation(message, bot)
        return

    user_entered_code = message.text.strip()

    if user_entered_code.isdigit() and int(user_entered_code) == sent_verification_code:
        email_request_message = (
            "📧 <b>Ви успішно підтвердили Вашу стару електронну скриньку. Тепер введіть нову електронну скриньку</b>\n\n"
            "❗ На Вашу електронну скриньку буде надіслано код підтвердження\n\n"
            "📝<b>Приклад електронної пошти:</b> example@example.com\n\n"
        )

        bot.send_message(message.chat.id, email_request_message, parse_mode='HTML',
                         reply_markup=cancel_mail_edit_markup)
        bot.register_next_step_handler(message, lambda msg: start_creating_user_mail(msg, bot, acc_id))

    else:
        invalid_code_message = "❌ <b>Неправильний код підтвердження</b> \n\n❗ Зміну електронної сриньки скасовано"
        bot.send_message(message.chat.id, invalid_code_message, parse_mode='HTML', reply_markup=keyboard_menu)
        return


def start_creating_user_mail(message, bot, acc_id):
    if message.text == "❌ Скасувати зміну скиньки":
        cancel_new_mail_creation(message, bot)
        return

    new_mail = message.text.strip()

    if not validate_email(new_mail):
        bot.send_message(message.chat.id, invalid_email_message, parse_mode='HTML',
                         reply_markup=cancel_mail_edit_markup)
        bot.register_next_step_handler(message, lambda msg: start_creating_user_mail(msg, bot, acc_id))
        return

    else:
        bot.send_message(message.chat.id, confirmation_code_message, parse_mode='HTML',
                         reply_markup=cancel_mail_edit_markup)
        verification_code = send_verification_code(new_mail)
        bot.register_next_step_handler(message, check_new_mail_verification_code, bot, acc_id, new_mail, verification_code)


def check_new_mail_verification_code(message, bot, acc_id, new_mail, sent_verification_code):
    if message.text == '❌ Скасувати зміну скриньки':
        cancel_new_mail_creation(message, bot)
        return

    user_entered_code = message.text.strip()

    if user_entered_code.isdigit() and int(user_entered_code) == sent_verification_code:
        new_mail_msg = '<b>❗ Ви успішно підтвердили Вашу нову електронну скриньку</b>'
        set_new_mail(acc_id, new_mail)
        bot.send_message(message.chat.id, new_mail_msg, parse_mode='HTML', reply_markup=keyboard_menu)
        new = show_user_profile_back(message)
        bot.send_message(message.chat.id, new, parse_mode='HTML',
                         reply_markup=profile_settings_markups)
    else:
        invalid_code_message = "❌ <b>Неправильний код підтвердження</b> \n\n❗ Зміну електронної сриньки скасовано"
        bot.send_message(message.chat.id, invalid_code_message, parse_mode='HTML', reply_markup=keyboard_menu)
        return


def cancel_new_mail_creation(message, bot):
    bot.send_message(message.chat.id, "<b>❗️ Зміну електронної скриньки скасовано</b>", parse_mode='HTML', reply_markup=keyboard_menu)

    # Скасування реєстрації наступних кроків
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)