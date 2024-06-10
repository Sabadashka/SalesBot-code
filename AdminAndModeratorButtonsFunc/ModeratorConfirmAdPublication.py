from DataBase.ModerationActions_database import create_action_moderator
from DataBase.Advertisement_database import get_all_info_about_advertisement, \
    change_status
from Markups.menu_markups import moderator_next_moderation
from Notifications.UserNotifications import notification_publication_ad_by_moderator, notification_delete_ad_by_moderator


def publish_ad(bot, call, ad_id, acc_id):
    info_ad = get_all_info_about_advertisement(ad_id)

    if info_ad:
        owner_telegram_id = info_ad[1]
        name = info_ad[4]
        name_markdown = f"*{name}*"

        bot.send_message(call.message.chat.id, "️❗️ Ми сповістили власника оголошення")

        bot.send_message(call.message.chat.id,
                         f"✅ Ви перевірили та опублікували оголошення '{name_markdown}'\nСтатус змінено на *published*",
                         parse_mode='Markdown', reply_markup=moderator_next_moderation)
        change_status(ad_id, 'published')
        create_action_moderator(acc_id, ad_id, 'published')
        notification_publication_ad_by_moderator(bot, owner_telegram_id, name)
    else:
        bot.send_message(call.message.chat.id, f"❗️ Не знайдено інформації про оголошення.")


def delete_ad(bot, call, ad_id, acc_id):
    info_ad = get_all_info_about_advertisement(ad_id)

    if info_ad:
        owner_telegram_id = info_ad[1]
        name = info_ad[4]
        name_markdown = f"*{name}*"

        bot.send_message(call.message.chat.id, "❗️ Ми сповістили власника оголошення!")

        bot.send_message(call.message.chat.id,
                         f"✅ Ви перевірили та дійшли до висновку видалити оголошення '{name_markdown}'\nСтатус змінено на *deleted*",
                         parse_mode='Markdown', reply_markup=moderator_next_moderation)

        change_status(ad_id, 'deleted')
        create_action_moderator(acc_id, ad_id, 'deleted')
        notification_delete_ad_by_moderator(bot, owner_telegram_id, name)

    else:
        bot.send_message(call.message.chat.id, f"❗️ Не знайдено інформації про оголошення.")