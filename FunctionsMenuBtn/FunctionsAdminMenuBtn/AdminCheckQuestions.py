from datetime import datetime

from telebot import types

from DataBase.Answer_database import create_answer_action
from DataBase.Questions_database import get_questions_with_status_none, set_status_question, get_info_question
from DataBase.Users_database import get_user_data
from Markups.menu_markups import moderator_menu_keyboard_menu, keyboard_menu, admin_menu_keyboard_menu, \
    admin_menu_database_keyboard_menu, admin_next_question, admin_question_exit
from Notifications.UserNotifications import create_answer_notification, reject_answer_notification
from OtherTools.MonthConverter import format_ukrainian_datetime_with_year_for_notifications


def check_questions(bot, message):
    acc_id = message.chat.id
    user_data = get_user_data(acc_id)
    questions_data = get_questions_with_status_none(acc_id)

    if not questions_data:
        role = user_data.get('role', 2)
        if role == 1:
            bot.send_message(message.chat.id, "❗️ Нові запитання відсутні", reply_markup=moderator_menu_keyboard_menu)
            return

        elif role == 2:
            bot.send_message(message.chat.id, "❗️ Нові запитання відсутні", reply_markup=admin_menu_keyboard_menu)
            return

        else:
            bot.send_message(message.chat.id, "❗️ У Вас немає таких прав", reply_markup=keyboard_menu)
            return

    else:
        bot.send_message(message.chat.id, "<b>❗️ Старайтеся оперативно відповідати на запитання</b>", parse_mode='HTML', reply_markup=admin_question_exit)

        for idx, question in enumerate(questions_data, start=1):
            new_status = f'on review {acc_id}'
            set_status_question(question[0], new_status)

            question_id = question[0]
            owner_question_id = question[1]
            question_text = question[2]
            question_date = question[4]

            date = format_ukrainian_datetime_with_year_for_notifications(question_date)
            question_message = (
                f"<b>❓ Запитання №{idx}</b>\n\n"
                f"<b>📝 Текст:</b> {question_text}\n\n"
                f"<i>❗️ Запитує:</i> <code>{owner_question_id}</code>\n"
                f"<b>{'-' * 40}</b>\n"
                f"<b>🗓 Дата:</b> {date}"
            )

            question_settings = types.InlineKeyboardMarkup(row_width=2)
            answer_button = types.InlineKeyboardButton("✅ Відповісти на питання",
                                                       callback_data=f'answer_button{question[0]}')
            reject_button = types.InlineKeyboardButton("❌ Відхилити питання",
                                                       callback_data=f'reject_button{question[0]}')
            question_settings.add(answer_button, reject_button)

            bot.send_message(message.chat.id, question_message, parse_mode='HTML', reply_markup=question_settings)

            break


def start_creating_answer(bot, call, acc_id, question_id):
    bot.send_message(call.message.chat.id, "<b>❗️ Введіть Вашу відповідь</b>", parse_mode='HTML')
    bot.register_next_step_handler(call.message, process_answer_text, bot, acc_id, question_id)


def process_answer_text(message, bot, acc_id, question_id):
    answer_text = message.text
    user_data = get_user_data(acc_id)
    question_data = get_info_question(question_id)

    if len(answer_text) > 350:
        bot.send_message(message.chat.id,
                         "<b>❗️ Відповідь не може бути більше 350 символів</b>\n\n⚠️ <i>Спробуйте ще раз</i>",
                         parse_mode='HTML')
        bot.register_next_step_handler(message, process_answer_text, bot, acc_id)

    else:
        if question_data:
            owner_question_id = question_data[1]
            question_text = question_data[2]

            question_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date = format_ukrainian_datetime_with_year_for_notifications(question_date)
            question_message = (
                f"<b>❗️ Вашу відповідь надіслано</b>\n\n"
                f"<b>📝 Відповідь:</b> {answer_text}\n\n"
                f"<b>{'-' * 40}</b>\n"
                f"<b>🗓 Дата:</b> {date}"
            )

            answer_final_text = f"<b>\n❓ Ваше запитання:</b> <i>{question_text}</i>\n\n <b>📝 Віповідь: {answer_text}</b>"

            role = user_data.get('role', 2)

            if role == 1:
                bot.send_message(message.chat.id, question_message, parse_mode='HTML',
                                 reply_markup=admin_next_question)
                create_answer_notification(bot, owner_question_id, question_id, answer_final_text)

                new_status = f'done'
                set_status_question(question_id, new_status)
                create_answer_action(acc_id, question_id, answer_text)

                return

            elif role == 2:
                bot.send_message(message.chat.id, question_message, parse_mode='HTML',
                                 reply_markup=admin_next_question)
                create_answer_notification(bot, owner_question_id, question_id, answer_final_text)

                new_status = f'done'
                set_status_question(question_id, new_status)
                create_answer_action(acc_id, question_id, answer_text)
                return

            else:
                bot.send_message(message.chat.id, "❗️ У Вас немає таких прав", reply_markup=keyboard_menu)
                return

        else:
            bot.send_message(message.chat.id, "❗️ Щось пішло не так... Запитання недоступне",
                             reply_markup=keyboard_menu)


def reject_answer(bot, call, acc_id, question_id):
    user_data = get_user_data(acc_id)
    role = user_data.get('role', 2)

    question_data = get_info_question(question_id)

    if question_data:
        owner_question_id = question_data[1]
        question_text = question_data[2]

        answer_final_text = f'\n<b>❓ Ваше запитання:</b> <i>"{question_text}</i>"\n\n<b>❌ Ваше запитання відхилено</b>'

        if role == 1:
            bot.send_message(call.message.chat.id, f"<b>❗️ Ви відхилили запитання №{question_id}</b>", parse_mode='HTML',
                             reply_markup=admin_next_question)

            new_status = f'done'
            set_status_question(question_id, new_status)
            reject_answer_notification(bot, owner_question_id, question_id, answer_final_text)

            answer_text = 'Відмова відповіді'
            create_answer_action(acc_id, question_id, answer_text)

            return

        elif role == 2:
            bot.send_message(call.message.chat.id, f"<b>❗️ Ви відхилили запитання №{question_id}</b>", parse_mode='HTML', reply_markup=admin_next_question)

            new_status = f'done'
            set_status_question(question_id, new_status)
            reject_answer_notification(bot, owner_question_id, question_id, answer_final_text)

            answer_text = 'Відмова відповіді'
            create_answer_action(acc_id, question_id, answer_text)

            return

        else:
            bot.send_message(call.message.chat.id, "❗️ У Вас немає таких прав", reply_markup=keyboard_menu)
            return

    else:
        bot.send_message(call.message.chat.id, "❗️ Щось пішло не так... Запитання недоступне", reply_markup=keyboard_menu)

