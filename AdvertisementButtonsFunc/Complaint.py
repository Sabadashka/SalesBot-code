from DataBase.Advertisement_database import get_all_info_about_advertisement
from DataBase.Complaints_database import is_advertisement_in_complaints, create_new_complaint
from Notifications.AdministratorNotifications import notification_complaint


def complaint(bot, call, ad_id, telegram_id):
    info = get_all_info_about_advertisement(ad_id)
    name = info[4]
    name_markdown = f"*{name}*"

    if not is_advertisement_in_complaints(telegram_id, ad_id):
        create_new_complaint(telegram_id, ad_id)
        bot.send_message(call.message.chat.id, f"⚠️ Ви поскаржились на оголошення '{name_markdown}'",
                         parse_mode='Markdown')

        notification_complaint(bot, telegram_id, name)

    else:
        bot.send_message(call.message.chat.id,
                         f"❌ Ви не можете поскаржитись більше 1 разу на оголошення '{name_markdown}'",
                         parse_mode='Markdown')