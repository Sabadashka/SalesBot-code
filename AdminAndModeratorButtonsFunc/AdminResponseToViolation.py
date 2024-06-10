from DataBase.Advertisement_database import get_all_info_about_advertisement, change_status
from DataBase.Complaints_database import set_status_for_ad_without_violation, \
    get_info_complaint_by_complaint_id
from Markups.menu_markups import admin_next_complaint
from Notifications.UserNotifications import notification_complaint_delete_ad_by_administrator, \
    notification_delete_ad_by_administrator, notification_complaint_no_violation_ad_by_administrator


def no_violation(bot, call, complaint_id):
    complaint_info = get_info_complaint_by_complaint_id(complaint_id)
    ad_id = complaint_info[2]
    info_ad = get_all_info_about_advertisement(ad_id)

    if info_ad:
        user_complained_id = complaint_info[1]
        name = info_ad[4]
        name_markdown = f"{name}"

        bot.send_message(call.message.chat.id, f"⚠️ Статус скарги на <b>'{name_markdown}'</b> було змінено на <b>done</b>",
                         parse_mode='HTML', reply_markup=admin_next_complaint)
        set_status_for_ad_without_violation(complaint_id, 'done')
        notification_complaint_no_violation_ad_by_administrator(bot, user_complained_id, name)

    else:
        bot.send_message(call.message.chat.id, f"Не знайдено інформації для скарги з id {complaint_id}.")


def yes_violation(bot, call, complaint_id):
    complaint_info = get_info_complaint_by_complaint_id(complaint_id)
    ad_id = complaint_info[2]
    info_ad = get_all_info_about_advertisement(ad_id)

    if info_ad:
        user_complained_id = complaint_info[1]
        user_owner_id = info_ad[1]

        name = info_ad[4]
        name_markdown = f"{name}"

        bot.send_message(call.message.chat.id, f"⚠️ Статус скарги на <b>'{name_markdown}'</b> було змінено на <b>deleted</b>>",
                         parse_mode='HTML', reply_markup=admin_next_complaint)

        set_status_for_ad_without_violation(complaint_id, 'deleted')
        change_status(ad_id, 'deleted')
        notification_complaint_delete_ad_by_administrator(bot, user_complained_id, name)
        notification_delete_ad_by_administrator(bot, user_owner_id, name)

    else:
        bot.send_message(call.message.chat.id, f"Не знайдено інформації для скарги з id {complaint_id}.")