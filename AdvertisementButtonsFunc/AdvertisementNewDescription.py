from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu, markup_ad_types
from DataBase.Advertisement_database import set_new_description_ad, change_status, \
    get_all_info_about_advertisement
from Notifications.ModeratorNotifications import notification_new_description_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes
from OtherTools.CancelAction import cancel_change_photos_ad_action, cancel_change_description_ad_action


def set_new_description_ad_btn(bot, call, ad_id, telegram_id):
    bot.send_message(call.message.chat.id, "<b>❗️ Введіть новий опис для оголошення</b>", parse_mode='HTML', reply_markup=cancel_action)

    bot.register_next_step_handler(call.message,
                                   lambda msg: process_new_description_ad_input(bot, msg, ad_id, telegram_id))


def process_new_description_ad_input(bot, message, ad_id, telegram_id):
    if message.text == '❌ Скасувати дію':
        cancel_change_description_ad_action(bot, message)
        return

    ad_info = get_all_info_about_advertisement(ad_id)
    new_description = message.text
    name = ad_info[4]
    old = ad_info[5]

    text = 'description_log'
    save_new_changes(ad_id, text, old, new_description)

    set_new_description_ad(ad_id, new_description)
    bot.send_message(message.chat.id, f"<b>✔️ Опис оголошення <i>'{name}'</i> змінено на <i>'{new_description}'</i></b>\n\n<i><b>📝 Примітка:</b> оголошення знаходиться на модерації. Наші модератори перевірять Ваше оголошення якнайшвидше і його зможуть побачити інші люди</i>",
                     parse_mode='HTML',
                     reply_markup=markup_ad_types)

    new_status = 'on moderation'
    change_status(ad_id, new_status)
    notification_new_description_ad(bot, name, telegram_id)
