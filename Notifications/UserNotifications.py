from DataBase.Advertisement_database import print_ads_for_deactivation
from DataBase.Notifications_database import create_notification


def notification_publication_ad_by_moderator(bot, telegram_id, name):
    bot.send_message(telegram_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = "Публікація оголошення"
    notification_text = f"Ми успішно перевірили Ваше оголошення та опублікували його! \n\n Оголошення <b>'{name}'</b> активне, інші користувачі можуть бачити його!"
    create_notification(telegram_id, notification_title, notification_text)


def notification_delete_ad_by_moderator(bot, telegram_id, name):
    bot.send_message(telegram_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = "Видалення оголошення"
    notification_text = (f"Ми перевірили Ваше оголошення та дійшли до висновку видалити його. Оголошення порушує "
                         f"правила створення оголошень.\n\n Оголошення: <b>'{name}'</b>")
    create_notification(telegram_id, notification_title, notification_text)


def notification_complaint_delete_ad_by_administrator(bot, telegram_id, name):
    bot.send_message(telegram_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = "Результат розгляду скарги"
    notification_text = (f"Ми перевірили Вашу скаргу на оголошення <b>'{name}'</b> та дійшли до висновку видалити його. "
                         f"\n\n<b>Дякуємо, що допомогаєте покращувати наш маркетплейс!</b>")
    create_notification(telegram_id, notification_title, notification_text)


def notification_complaint_no_violation_ad_by_administrator(bot, telegram_id, name):
    bot.send_message(telegram_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = "Результат розгляду скарги"
    notification_text = (f"Ми перевірили Вашу скаргу на оголошення <b>'{name}'</b> та дійшли до висновку, що оголошення не порушує правила створення оголошень. "
                         f"\n\n<b>Дякуємо, що допомогаєте покращувати наш маркетплейс!</b>")
    create_notification(telegram_id, notification_title, notification_text)


def notification_delete_ad_by_administrator(bot, telegram_id, name):
    bot.send_message(telegram_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = "Видалення оголошення"
    notification_text = (f"На Ваше оголошення <b>'{name}</b>' надійшла скарга. Ми успішно перевірили його та дійшли до висновку видалити його. Оголошення порушує правила створення оголошень")
    create_notification(telegram_id, notification_title, notification_text)


def make_notification_by_administrator(bot, telegram_id, notification_title, notification_text):
    bot.send_message(telegram_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    create_notification(telegram_id, notification_title, notification_text)


def create_answer_notification(bot, acc_id, question_id, answer_text):
    bot.send_message(acc_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = f"Відповідь на запитання №{question_id}"
    create_notification(acc_id, notification_title, answer_text)


def reject_answer_notification(bot, acc_id, question_id, answer_text):
    bot.send_message(acc_id, "<b>🔔️ У Вас нове сповіщення</b>", parse_mode='HTML')
    notification_title = f"Відхилено запитання №{question_id}"
    create_notification(acc_id, notification_title, answer_text)

