from DataBase.Advertisement_database import set_new_name_ad, change_status, \
    get_all_info_about_advertisement
from Markups.markups import cancel_action
from Markups.menu_markups import keyboard_menu
from Notifications.ModeratorNotifications import notification_new_name_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes
from OtherTools.CancelAction import cancel_change_new_name_ad_action


def set_new_name_ad_btn(bot, call, ad_id, telegram_id):
    bot.send_message(call.message.chat.id, "<b>❗️ Введіть нове ім'я для оголошення</b>", parse_mode='HTML', reply_markup=cancel_action)

    bot.register_next_step_handler(call.message, lambda msg: process_new_name_ad_input(bot, msg, ad_id, telegram_id))


def process_new_name_ad_input(bot, message, ad_id, telegram_id):
    if message.text == '❌ Скасувати дію':
        cancel_change_new_name_ad_action(bot, message)
        return

    ad_info = get_all_info_about_advertisement(ad_id)
    new_name = message.text
    name = ad_info[4]

    text = 'name_log'
    save_new_changes(ad_id, text, name, new_name)

    set_new_name_ad(ad_id, new_name)
    bot.send_message(message.chat.id, f"<b>✔️ Назву оголошення <i>'{name}'</i> змінено на <i>'{new_name}'</i></b>\n\n<i><b>📝 Примітка:</b> оголошення знаходиться на модерації. Наші модератори перевірять Ваше оголошення якнайшвидше і його зможуть побачити інші люди</i>", parse_mode='HTML',
                     reply_markup=keyboard_menu)

    new_status = 'on moderation'
    change_status(ad_id, new_status)
    notification_new_name_ad(bot, name, telegram_id)

