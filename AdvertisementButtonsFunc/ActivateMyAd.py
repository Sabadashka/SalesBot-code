from DataBase.Advertisement_database import get_all_info_about_advertisement, change_status_with_new_time
from Notifications.ModeratorNotifications import notification_activation_ad
from OtherTools.AdvertisementChangesLogging import save_new_changes


def activate_my_ad(bot, call, ad_id):
    info = get_all_info_about_advertisement(ad_id)

    if info is not None:
        owner_id = info[1]
        name = info[4]
        name_markdown = f"*{name}*"

        message_id = call.message.message_id
        bot.send_message(call.message.chat.id, f"❗️ Ви усішно активували своє оголошення '{name_markdown}'",
                         parse_mode='Markdown')
        bot.delete_message(call.message.chat.id, message_id)

        new_status = 'on moderation'
        change_status_with_new_time(ad_id, new_status)
        notification_activation_ad(bot, name, owner_id)

        text = 'activate_log'
        save_new_changes(ad_id, text, old=None, new=None)
    else:
        bot.send_message(call.message.chat.id, "❗️ Помилка при отриманні інформації про оголошення. Спробуйте ще раз.")
