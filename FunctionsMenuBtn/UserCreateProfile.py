from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from telebot import TeleBot

from DataBase.Users_database import create_new_user
from OtherTools.CancelAction import cancel_registration_button

from Markups.markups import cancel_reg_btn
from Messages.StartBotMessages import name_request_message, name_error_message, email_request_message, \
    invalid_email_message, confirmation_code_message, send_message_with_user_mail, phone_request_message, \
    phone_error_request_message, invalid_code_message
from Validation.NameValidation import validate_name
from Validation.MailValidation import validate_email
from Mail.MailVerification import send_verification_code


def start_creating_user(bot: TeleBot, message: Message):
    bot.send_message(message.chat.id, name_request_message, parse_mode='HTML', reply_markup=cancel_reg_btn)
    bot.register_next_step_handler(message, start_creating_user_name, bot)


def phone_number_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("📱 Поділитися номером телефону", request_contact=True)
    keyboard.add(button)
    return keyboard


def start_creating_user_name(message: Message, bot: TeleBot):
    if message.text == '❌ Скасувати реєстрацію':
        cancel_registration_button(message, bot)
        return

    name = message.text.strip()
    acc_id = message.chat.id

    if not validate_name(name):
        bot.send_message(message.chat.id, name_error_message, parse_mode='HTML', reply_markup=cancel_reg_btn)
        bot.register_next_step_handler(message, lambda msg: start_creating_user_name(msg, bot))
        return

    else:
        bot.send_message(message.chat.id, phone_request_message, parse_mode='HTML', reply_markup=phone_number_keyboard())
        bot.register_next_step_handler(message, start_creating_user_phone_number, bot, acc_id, name)


def start_creating_user_phone_number(message: Message, bot: TeleBot, acc_id: str, name: str):
    if message.text == '❌ Скасувати реєстрацію':
        cancel_registration_button(message, bot)
        return

    if message.contact:
        phone_number = message.contact.phone_number
        bot.send_message(message.chat.id, email_request_message, parse_mode='HTML', reply_markup=cancel_reg_btn)
        bot.register_next_step_handler(message, start_creating_user_mail, bot, acc_id, name, phone_number)
    else:
        bot.send_message(message.chat.id, phone_error_request_message, parse_mode='HTML', reply_markup=phone_number_keyboard())
        bot.register_next_step_handler(message, start_creating_user_phone_number, bot, acc_id, name)


def start_creating_user_mail(message: Message, bot: TeleBot, acc_id: str, name: str, phone_number: str):
    if message.text == '❌ Скасувати реєстрацію':
        cancel_registration_button(message, bot)
        return

    mail = message.text.strip()

    if not validate_email(mail):
        bot.send_message(message.chat.id, invalid_email_message, parse_mode='HTML',
                         reply_markup=cancel_reg_btn)
        bot.register_next_step_handler(message, lambda msg: start_creating_user_mail(msg, bot, acc_id, name, phone_number))
        return

    else:
        bot.send_message(message.chat.id, confirmation_code_message, parse_mode='HTML',
                         reply_markup=cancel_reg_btn)
        verification_code = send_verification_code(mail)
        bot.register_next_step_handler(message, check_verification_code, bot, acc_id, name, phone_number, mail, verification_code)


def check_verification_code(message: Message, bot: TeleBot, acc_id: str, name: str, phone_number: str, mail: str,
                            sent_verification_code: int):
    if message.text == '❌ Скасувати реєстрацію':
        cancel_registration_button(message, bot)
        return

    user_entered_code = message.text.strip()
    if user_entered_code.isdigit() and int(user_entered_code) == sent_verification_code:
        send_message_with_user_mail(bot, message, mail)
        create_new_user(acc_id, name, mail, phone_number)
    else:
        bot.send_message(message.chat.id, invalid_code_message, parse_mode='HTML', reply_markup=cancel_reg_btn)
        bot.register_next_step_handler(message, check_verification_code, bot, acc_id, name, phone_number, mail,
                                       sent_verification_code)