from DataBase.Advertisement_database import get_all_info_about_advertisement, change_status, \
    change_date_for_extend_advertisement
from DataBase.Notified_database import delete_notified_user, get_notified_id_by_ids
from Markups.menu_markups import markup_ad_types
from Notifications.ModeratorNotifications import notification_new_description_ad, notification_extend_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes


def extend_my_ad(bot, message, chat_id, ad_id):
    ad_info = get_all_info_about_advertisement(ad_id)
    name = ad_info[4]

    msg = f'<b>❗️ Оголошення {name} активовано ще на 30 днів </b>\n\n<i><b>📝 Примітка:</b> оголошення знаходиться на модерації. Наші модератори перевірять Ваше оголошення якнайшвидше і його зможуть побачити інші люди</i>'
    bot.send_message(message.chat.id, msg, parse_mode='HTML', reply_markup=markup_ad_types)

    text = 'extend_log'
    save_new_changes(ad_id, text, old=None, new=None)
    change_date_for_extend_advertisement(ad_id)

    notified_id = get_notified_id_by_ids(ad_id)
    delete_notified_user(notified_id)

    new_status = 'on moderation'
    change_status(ad_id, new_status)
    notification_extend_ad(bot, name, chat_id)
