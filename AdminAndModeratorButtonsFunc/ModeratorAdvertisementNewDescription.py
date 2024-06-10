from DataBase.Advertisement_database import set_new_description_ad, change_status, \
    get_all_info_about_advertisement
from Markups.menu_markups import keyboard_menu, moderator_moderation_exit


def moderator_set_new_description_ad(bot, call, ad_id):

    info_ad = get_all_info_about_advertisement(ad_id)

    name_ad = info_ad[4]
    bot.send_message(call.message.chat.id, f"❗️ *[MODERATOR]* Введіть новий опис для оголошення *'{name_ad}'*", parse_mode='Markdown')

    bot.register_next_step_handler(call.message, lambda msg: moderator_process_new_description_ad_input(bot, msg, ad_id))


def moderator_process_new_description_ad_input(bot, message, ad_id):
    new_description = message.text

    set_new_description_ad(ad_id, new_description)
    bot.send_message(message.chat.id, f"❗️ *[MODERATOR]* Опис оголошення змінено на '*{new_description}*'", parse_mode='Markdown',
                     reply_markup=moderator_moderation_exit)