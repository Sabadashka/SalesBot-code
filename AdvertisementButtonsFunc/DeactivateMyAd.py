from DataBase.Advertisement_database import get_all_info_about_advertisement, change_status
from OtherTools.AdvertisementChangesLogging import save_new_changes


def deactivate_my_ad(bot, call, ad_id):
    info = get_all_info_about_advertisement(ad_id)

    if info is not None:
        name = info[4]
        name_markdown = f"*{name}*"

        message_id = call.message.message_id
        bot.send_message(call.message.chat.id, f"❗️ Ви усішно деактивували своє оголошення '{name_markdown}'",
                         parse_mode='Markdown')

        bot.delete_message(call.message.chat.id, message_id)

        new_status = 'deactivated'
        change_status(ad_id, new_status)

        text = 'deactivate_log'
        save_new_changes(ad_id, text, old=None, new=None)
    else:
        bot.send_message(call.message.chat.id, "❗️ Помилка при отриманні інформації про оголошення. Спробуйте ще раз.")
