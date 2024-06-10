from DataBase.Advertisement_database import get_all_info_about_advertisement, set_new_price_ad, \
    change_status
from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu, markup_ad_types
from Notifications.ModeratorNotifications import notification_new_price_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes
from OtherTools.CancelAction import cancel_change_price_ad_action


def set_new_price_ad_btn(bot, call, ad_id, telegram_id):
    bot.send_message(call.message.chat.id, "<b>❗️ Введіть нову ціну для оголошення</b>", parse_mode='HTML', reply_markup=cancel_action)

    bot.register_next_step_handler(call.message, lambda msg: process_new_price_ad_input(bot, msg, ad_id, telegram_id))


def process_new_price_ad_input(bot, message, ad_id, telegram_id):
    if message.text == "❌ Скасувати дію":
        cancel_change_price_ad_action(bot, message)
        return

    ad_info = get_all_info_about_advertisement(ad_id)
    try:
        new_price = float(message.text)

        if new_price < 0 or new_price > 100000000:
            bot.send_message(message.chat.id, "❗️ Ціна оголошення повинна бути в межах від 0 до 100000000.")
            bot.register_next_step_handler(message, lambda m: process_new_price_ad_input(bot, m, ad_id, telegram_id))

        else:
            name = ad_info[4]
            old = ad_info[7]

            text = 'price_log'
            save_new_changes(ad_id, text, old, new_price)

            set_new_price_ad(ad_id, new_price)
            bot.send_message(message.chat.id, f"<b>✔️ Ціну оголошення <i>'{name}'</i> змінено  з <i>'{old}'</i> на <i>'{new_price}'</i></b>\n\n<i><b>📝 Примітка:</b> оголошення знаходиться на модерації. Наші модератори перевірять Ваше оголошення якнайшвидше і його зможуть побачити інші люди</i>",
                             parse_mode='HTML',
                             reply_markup=markup_ad_types)

            new_status = 'on moderation'
            change_status(ad_id, new_status)
            notification_new_price_ad(bot, name, telegram_id)

    except ValueError:
        bot.send_message(message.chat.id, "❗️ Некоректне значення ціни. Введіть числове значення.")
        bot.register_next_step_handler(message, lambda m: process_new_price_ad_input(bot, m, ad_id, telegram_id))
