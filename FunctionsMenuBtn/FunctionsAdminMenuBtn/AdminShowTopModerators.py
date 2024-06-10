from DataBase.Answer_database import get_top_moderators_by_answers
from DataBase.ModerationActions_database import get_top_moderators_by_moderation
from DataBase.Users_database import get_user_data_by_telegram_id


def pluralize_word(number, word1, word2):
    if 1 <= number <= 4:
        return f"{number} {word1} {word2}"
    else:
        return f"{number} {word1[:-2]}ь {word2}"


def show_top_moderators_by_moderation(bot, message):
    print_show_top_moderators_by(bot, message, get_top_moderators_by_moderation()[:5], "🌟 ТОП-5 Модераторів [Перевірка оголошень]")


def show_top_moderators_by_answers(bot, message):
    print_show_top_moderators_by(bot, message, get_top_moderators_by_answers()[:5],
                        "🌟 ТОП-5 Модераторів [Відповіді на запитання]")


def print_show_top_moderators_by(bot, message, top_moderators, title):
    if top_moderators:
        top = f"<b>{title}:</b>\n\n"  # Додавання заголовка

        for i, (telegram_id, actions_count) in enumerate(top_moderators, start=1):
            user_data = get_user_data_by_telegram_id(telegram_id)

            if user_data:
                name = user_data[1]
                divider = f"{'-' * 30}"

                place_symbols = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                place = place_symbols[i - 1]

                top += f"{place} <code>{telegram_id}</code> | <b>{name}</b> \n<b>Кількість:</b> {actions_count}\n{divider}\n"

        bot.send_message(message.chat.id, top, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "🤷‍♂️ <b>Наразі немає модераторів в рейтингу</b>", parse_mode='HTML')
